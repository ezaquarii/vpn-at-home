from channels.generic.websocket import AsyncJsonWebsocketConsumer
from vpnathome import get_bin_path
from vpnathome.utils import SubprocessThread
from vpnathome.apps.management.serializers import BlockListUrlUpdateSerializer

import asyncio


class CommandError(Exception):

    def __init__(self, message):
        super().__init__(message)


class GenericProcessRunnerConsumer(AsyncJsonWebsocketConsumer):

    STATUS_STARTED = 'started'
    STATUS_FINISHED = 'finished'
    STATUS_RUNNING = 'running'
    STATUS_ERROR = 'error'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.process = None
        self.output = []
        self.flush_task = None

    def _post(self, func, *args, **kwargs):
        asyncio.run_coroutine_threadsafe(func(*args, **kwargs), self.loop)

    async def on_stdout(self, line):
        self.output.append(line)

    async def on_stderr(self, line):
        self.output.append(line)

    async def on_finished(self):
        self.flush_task.cancel()
        await self.send_output()
        await self.send_json({
            'status': self.STATUS_FINISHED
        })

    async def flush(self):
        while True:
            await asyncio.sleep(1)
            await self.send_output()

    async def send_output(self):
        if len(self.output) > 0:
            message = {'status': self.STATUS_RUNNING, 'output': self.output}
            self.output = []
            await self.send_json(message)

    async def connect(self):
        self.loop = asyncio.get_event_loop()
        await self.accept()

    async def receive_json(self, content, **kwargs):
        cmd = content.get('cmd', None)
        args = content.get('args', {})
        if type(cmd) is not str or type(args) is not dict:
            await self.close()
        elif cmd == 'start':
            await self.cmd_start(**args)
        elif cmd == 'stop':
            await self.cmd_stop()
        else:
            print(f"Unknown command {cmd}, content: {content}, kwargs: {kwargs}")

    async def disconnect(self, code):
        await self.cmd_stop()
        await super().disconnect(code)

    def get_process_command(self, **kwargs):
        raise NotImplementedError()

    def pre_process_start(self, **kwargs):
        pass

    async def cmd_start(self, **kwargs):
        if self.process:
            await self.send_json({'status': self.STATUS_ERROR, 'message': 'already running'})

        try:
            cmd = self.get_process_command(**kwargs)
            self.process = SubprocessThread(
                cmd=cmd,
                on_stdout=lambda line: self._post(self.on_stdout, line),
                on_stderr=lambda line: self._post(self.on_stderr, line),
                on_finished=lambda: self._post(self.on_finished),
            )
            self.process.start()
            self.flush_task = asyncio.ensure_future(self.flush())
            await self.send_json({'status': self.STATUS_STARTED})
        except Exception as e:
            await self.send_json({'status': self.STATUS_ERROR, 'message': str(e)})

    async def cmd_stop(self):
        if self.flush_task:
            self.flush_task.cancel()
            self.flush_task = None
        if self.process:
            self.process.stop()
            self.process = None


class DeploymentConsumer(GenericProcessRunnerConsumer):

    async def on_stderr(self, line):
        # This [ERROR]: is harmless ansible bug
        if len(self.output) == 0 and line == '[ERROR]:':
            pass
        else:
            await super().on_stderr(line)

    def get_process_command(self, **kwargs):
        hostname = kwargs.get('hostname', None)
        if not hostname:
            raise CommandError('invalid hostname')
        return [get_bin_path("deploy_vpn.sh"), "--host", hostname]


class UpdateBlockLists(GenericProcessRunnerConsumer):

    def get_process_command(self, **kwargs):
        serializer = BlockListUrlUpdateSerializer(data=kwargs.get('sources', None), many=True, require_id=True)
        if not serializer.is_valid():
            raise CommandError("Invalid argument")

        def is_enabled(item): return item['enabled']

        def to_id_str(item): return str(item['id'])

        enabled_sources_ids = map(to_id_str, filter(is_enabled, serializer.validated_data))
        cmd = ["manage.py", "update_block_list", *enabled_sources_ids]
        return cmd
