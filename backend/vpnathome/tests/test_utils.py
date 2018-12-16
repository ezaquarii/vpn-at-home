from unittest import TestCase
from vpnathome.tests import APITestWithBaseFixture
from vpnathome import get_bin_path
from vpnathome.utils import get_nested_item
from vpnathome.utils import is_database_migrated, SubprocessThread

import asyncio


class TestGetNestedItem(TestCase):

    obj = {'a': {'b': {'c': 1}}}

    def test_get_existing_item(self):
        item = get_nested_item(self.obj, 'a.b.c')
        self.assertEqual(item, 1)

    def test_get_nonexisting_item_1(self):
        try:
            item = get_nested_item(self.obj, 'a.b.c.d')
            self.fail()
        except KeyError:
            pass

    def test_get_nonexisting_item_2(self):
        try:
            item = get_nested_item(self.obj, 'a.b.x')
            self.fail()
        except KeyError:
            pass


class TestIsDatabaseMigrated(APITestWithBaseFixture):

    def test_is_migrated(self):
        self.assertTrue(is_database_migrated())

    def test_unknown_database_is_not_migrated(self):
        self.assertFalse(is_database_migrated('unknown-database'))


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestSubprocessThread(TestCase):

    ITERATIONS = 3

    def on_stdout(self, line):
        self.stdout.append(line)

    def on_stderr(self, line):
        self.stderr.append(line)

    def on_finished(self):
        self.finished = True

    def setUp(self):
        from .helpers import PROCESS_PY_PATH
        self.cmd = ["python3", PROCESS_PY_PATH, '--stdout', '--stderr', '--iterations', str(self.ITERATIONS)]
        self.stderr = []
        self.stdout = []
        self.finished = False

        self.process_thread = SubprocessThread(
            cmd=self.cmd,
            on_stderr=self.on_stderr,
            on_stdout=self.on_stdout,
            on_finished=self.on_finished
        )

        self.process_thread.start()
        self.process_thread.join(10)
        self.assertFalse(self.process_thread.is_alive())

    def test_callbacks_fired(self):
        self.assertEqual(self.ITERATIONS, len(self.stdout))
        self.assertEqual(self.ITERATIONS, len(self.stderr))
        self.assertTrue(self.finished)
