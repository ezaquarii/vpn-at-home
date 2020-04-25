from os import getcwd, environ
from os.path import abspath, dirname, join
from distutils.sysconfig import get_python_lib


def get_virtual_env_path():
    return environ.get('VIRTUAL_ENV') or abspath(join(get_python_lib(), '../../../'))


VIRTUALENV_PATH = get_virtual_env_path()
ROOT_DIR = abspath(join(VIRTUALENV_PATH, '..'))
MAIN_PKG_DIR = dirname(__file__)
DATA_DIR = join(getcwd(), 'data')
FRONTEND_DIR = abspath(join(ROOT_DIR, 'frontend'))  # we need to get out of venv into root dirs
VERSION = "2.1.1"


def get_virtual_env_path():
    return environ.get('VIRTUAL_ENV') or abspath(join(get_python_lib(), '../../../'))


def get_root_path(file_path):
    """
    Get path from project's root directory.

    :param file_path: File path relative to project's root directory
    :return: Absolute path to file or dir
    """
    return abspath(join(VIRTUALENV_PATH, '..', file_path))


def get_bin_path(file_path):
    """
    Get path from project's bin directory. bin contains
    various scripts.

    :param file_path: File path relative to project's bin directory
    :return: Absolute path to file or dir
    """
    venv = get_virtual_env_path()
    return abspath(join(venv, 'bin', file_path))


def get_frontend_path(file_path):
    """
    Get path from frontend directory.

    :param file_path: File path relative to frontend directory
    :return: Absolute path to file or dir
    """
    return abspath(join(FRONTEND_DIR, file_path))


def get_data_path(file_path, make_dirs=False):
    """
    Get path from project's data directory.

    :param file_path: File path relative to project's data directory
    :param make_dirs: Create required directories
    :return: Absolute path to file or dir
    """

    return abspath(join(DATA_DIR, file_path))


def ensure_path_dirs(file_path, mode=0o750):
    import os
    dir_path = dirname(file_path)
    os.makedirs(dir_path, mode=mode, exist_ok=True)
