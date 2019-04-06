from os import getcwd, environ
from os.path import abspath, dirname, join

MAIN_PKG_DIR = dirname(__file__)
ROOT_DIR = abspath(join(dirname(__file__), '../..'))
VIRTUAL_ENV_DIR = environ.get('VIRTUAL_ENV') or ''
DATA_DIR = join(getcwd(), 'data')
FRONTEND_DIR = abspath(join(ROOT_DIR, '../../../', 'frontend')) # we need to get out of venv into root dirs
VERSION = "2.0.0"


def get_root_path(file_path):
    """
    Get path from project's root directory.

    :param file_path: File path relative to project's root directory
    :return: Absolute path to file or dir
    """
    return abspath(join(ROOT_DIR, file_path))


def get_bin_path(file_path):
    """
    Get path from project's bin directory. bin contains
    various scripts.

    :param file_path: File path relative to project's bin directory
    :return: Absolute path to file or dir
    """
    venv = environ.get('VIRTUAL_ENV') or ''
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
