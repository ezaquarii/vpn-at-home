from os.path import abspath, dirname, join

MAIN_PKG_DIR = dirname(__file__)
ROOT_DIR = abspath(join(dirname(__file__), '../..'))
DATA_DIR = join(ROOT_DIR, 'data')
BASE_DIR = join(ROOT_DIR, 'backend')
BACKEND_DIR = BASE_DIR
BIN_DIR = join(ROOT_DIR, 'bin')
FRONTEND_DIR = join(ROOT_DIR, 'frontend')
CONFIG_PATH = join(MAIN_PKG_DIR, 'config.py')
CONFIG_TEMPLATE_PATH = join(MAIN_PKG_DIR, 'config.py.example')
VERSION = "1.8.0"


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
    return abspath(join(BIN_DIR, file_path))


def get_backend_path(file_path):
    """
    Get path from backend directory.

    :param file_path: File path relative to backend directory
    :return: Absolute path to file or dir
    """
    return abspath(join(BACKEND_DIR, file_path))


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
