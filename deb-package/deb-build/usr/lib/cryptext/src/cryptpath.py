import os
from pathlib import Path


def _create_dir(dir):
    os.mkdir(dir)


def _ensure_crypt_path(dir_name):
    dir = os.path.join(str(Path.home()), dir_name)
    if not os.path.exists(dir):
        _create_dir(dir)
    return dir


CRYPTPATH = _ensure_crypt_path('.cryptext')
