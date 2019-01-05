"""
This module provides generic utility functions, not related to any
specific business functionality.
"""
from operator import attrgetter as _attrgetter
import subprocess
import threading
from django.core.validators import ValidationError


def get_nested_item(obj, path):
    keys = path.split('.')
    try:
        for key in keys:
            obj = obj[key]
        return obj
    except Exception:
        raise KeyError(path)


def get_nested_attr(obj, path, default_value=None, raise_exception=False):
    """
    Get nested object property. It uses ``operator.attrgetter`` internally.

    :param obj: Object (top-level)
    :param path: Path to property. See
    :param default_value: Default value returned when attribute is not present.
    :param raise_exception: If True, raise exception instead of returning a default value
    :return: Attribute value or default value, if attribute is not present
    """
    getter = _attrgetter(path)
    try:
        return getter(obj)
    except AttributeError as e:
        if raise_exception:
            raise e
        else:
            return default_value


def get_attr_or_throw(obj, name, message):
    if hasattr(obj, name):
        return getattr(obj, name)
    else:
        raise AttributeError(message)


def get_object_or_none(klass, *args, **kwargs):
    """
    Use get() to return an object, or return None if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    try:
        return klass.objects.get(*args, **kwargs)
    except:
        return None


def filter_objects_to_map_by_pk(klass, **kwargs):
    """
    Use filter() on a given model manager, but return a map of items by pk

    :param klass:
    :param kwargs:
    :return: map of items by pk
    """
    return {item.pk: item for item in klass.objects.filter(**kwargs)}


def user_input(msg, default=None, validator=None):
    """
    Displays prompt and allows user to enter some data.

    A validator can be either Django Validator (throwing exceptions)
    or functor returning True/False.

    :param msg: Prompt message. It will be appended with ':'
    :param default: default value, if user doesn't enter anything
    :param validator: Validator that checks entry string, predicate or throwing exception
    :return: value typed by user
    """

    def validated_or_throw(input, default, validator=None):
        value = input if input else default
        validation_result = validator(value) if validator is not None else True
        if validation_result in [True, None]:
            return value
        else:
            raise ValidationError('{} validation failed'.format(value))

    prompt = '{msg} [{default}]: '.format(msg=msg, default=default) if default else '{msg}: '.format(msg=msg)

    while True:
        result = input(prompt)
        try:
            return validated_or_throw(result, default, validator)
        except Exception as ex:
            print('Please enter correct value')
            continue


def is_database_migrated(database='default'):
    from django.db import connections
    from django.db.migrations.loader import MigrationLoader
    if database in connections:
        loader = MigrationLoader(connections[database])
        all_migrations = loader.graph.nodes.keys()
        applied = loader.applied_migrations
        return all([migration in applied for migration in all_migrations])
    else:
        return False


class _StreamReaderThread(threading.Thread):

    def __init__(self, stream, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream = stream
        self.callback = callback

    def run(self):
        for raw_line in iter(self.stream.readline, b''):
            line = raw_line.decode('utf8')
            self.callback(line.strip())


class SubprocessThread(threading.Thread):

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
        try:
            self._process = subprocess.Popen(self._cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self._stdout_reader_thread = _StreamReaderThread(stream=self._process.stdout, callback=self._on_stdout)
            self._stderr_reader_thread = _StreamReaderThread(stream=self._process.stderr, callback=self._on_stderr)
            self._stdout_reader_thread.start()
            self._stderr_reader_thread.start()
            self._process.wait()
            self._stdout_reader_thread.join()
            self._stdout_reader_thread.join()
        except Exception as e:
            self._on_stderr(str(e))
        finally:
            self._on_finished()

    def stop(self):
        # could be None of Popen fails
        if self._process is not None:
            self._process.terminate()
            self._process.wait()
        self.join()
