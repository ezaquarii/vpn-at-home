import subprocess
import threading


class _StreamReaderThread(threading.Thread):

    def __init__(self, stream, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream = stream
        self.callback = callback

    def run(self):
        for raw_line in iter(self.stream.readline, b''):
            line = raw_line.decode('utf8')
            self.callback(line.strip())


class ThreadedSubprocess(threading.Thread):

    def __init__(self, cmd, on_stdout=None, on_stderr=None, on_finished=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cmd = cmd
        self._process = None
        self._on_stdout = on_stdout
        self._on_stderr = on_stderr
        self._on_finished = on_finished
        self._stdout_reader_thread = None
        self._stderr_reader_thread = None

    def run(self):
        self._process = subprocess.Popen(self._cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._stdout_reader_thread = _StreamReaderThread(stream=self._process.stdout, callback=self._on_stdout)
        self._stderr_reader_thread = _StreamReaderThread(stream=self._process.stderr, callback=self._on_stderr)
        self._stdout_reader_thread.start()
        self._stderr_reader_thread.start()
        self._process.wait()
        self._stdout_reader_thread.join()
        self._stdout_reader_thread.join()
        self._on_finished()


ts = ThreadedSubprocess(["../bin/process.py", "--stdout", "--stderr"])
ts.start()
ts.join()

