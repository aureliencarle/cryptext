import os
from pathlib import Path


def _create_dir(dir):
    os.mkdir(dir)


HOME = str(Path.home())


def _ensure_crypt_path(dir_name):
    dir = os.path.join(HOME, dir_name)
    if not os.path.exists(dir):
        _create_dir(dir)
    return dir


CRYPTPATH = _ensure_crypt_path('.cryptext')
PLUGPATH = 'plugin'
PASSPATH = 'core'
