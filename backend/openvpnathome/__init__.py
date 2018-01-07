from os.path import abspath, dirname, join

MAIN_PKG_DIR = dirname(__file__)
ROOT_DIR = abspath(join(dirname(__file__), '../..'))
BASE_DIR = join(ROOT_DIR, 'backend')
BACKEND_DIR = BASE_DIR
FRONTEND_DIR = join(ROOT_DIR, 'frontend')
CONFIG_PATH = join(MAIN_PKG_DIR, 'config.py')
CONFIG_TEMPLATE_PATH = join(MAIN_PKG_DIR, 'config.py.example')


def get_root_path(file_path):
    """
    Get path from project's root directory.

    :param file_path: File path relative to project's root directory
    :return: Absolute path to file or dir
    """
    return abspath(join(ROOT_DIR, file_path))


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
