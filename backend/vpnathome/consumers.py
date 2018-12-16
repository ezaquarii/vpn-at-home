from channels.generic.websocket import AsyncJsonWebsocketConsumer

from vpnathome import get_bin_path
from vpnathome.utils import SubprocessThread

import asyncio


class ProcessRunnerConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.process = None
        self.output = []
        self.flush_task = None

    def post(self, func, *args, **kwargs):
        asyncio.run_coroutine_threadsafe(func(*args, **kwargs), self.loop)

    async def on_stdout(self, line):
        self.output.append(line)

    async def on_stderr(self, line):
        self.output.append(line)

    async def on_finished(self):
        self.flush_task.cancel()
        await self.send_output()
        await self.send_json({
            'status': 'finish'
        })

    async def flush(self):
        while True:
            await asyncio.sleep(1)
            await self.send_output()

    async def send_output(self):
        if len(self.output) > 0:
            message = {'status': 'running', 'output': self.output}
            self.output = []
            await self.send_json(message)

    async def connect(self):
        self.loop = asyncio.get_event_loop()
        await self.accept()

    async def receive_json(self, content, **kwargs):
        cmd = content['cmd']
        if cmd == 'start':
            await self.cmd_start(**content['args'])
        elif cmd == 'stop':
            await self.cmd_stop()

    async def disconnect(self, code):
        await self.cmd_stop()
        await super().disconnect(code)

    async def cmd_start(self, hostname=None, **kwargs):
        if self.process:
            await self.send(({'message': 'already running'}))
        elif hostname is None:
            await self.send(({'message': 'invalid hostname'}))
        else:
            cmd = [get_bin_path("deploy_vpn.sh"), "--host", hostname]
            self.process = SubprocessThread(
                cmd=cmd,
                on_stdout=lambda line: self.post(self.on_stdout, line),
                on_stderr=lambda line: self.post(self.on_stderr, line),
                on_finished=lambda: self.post(self.on_finished),
            )
            self.process.start()
            self.flush_task = asyncio.ensure_future(self.flush())
            await self.send_json({'status': 'start'})

    async def cmd_stop(self):
        if self.flush_task:
            self.flush_task.cancel()
            self.flush_task = None
        if self.process:
            self.process.stop()
            self.process = None
