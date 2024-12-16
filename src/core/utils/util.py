import datetime
import json
import os
import pickle
import shutil
import time
from collections import defaultdict

from loguru import logger


@logger.catch
def dump_json(data, path, sort_keys=False):
    """Write data as json file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w+', encoding='utf8') as file_object:
        json.dump(data, file_object, indent=4, sort_keys=sort_keys)
    logger.debug(f'Write json file, data: {type(data)}, path: {path}')


def load_json(path):
    """Read json file"""
    logger.debug(f'Read json file, path: {path}')
    try:
        with open(path, 'r', encoding='utf8') as file_object:
            data = json.load(file_object)
        return data
    except Exception:
        return None


def is_json(path):
    """Check if valid json file"""
    try:
        load_json(path)
    except Exception:
        return False
    return True


@logger.catch
def dump_log(case_name, state, error, export_path, file_name):
    file_path = os.path.join(export_path, case_name)
    os.makedirs(file_path, exist_ok=True)
    time_stamp = datetime.datetime.now()
    message = f'\n{time_stamp}\n\t{state}: \n\t\t{error}\n'
    with open(os.path.join(file_path, f'{file_name}_log.txt'), 'a+', encoding='utf8') as file_object:
        file_object.write(message)
    logger.warning(f'Dumped {file_name} log with message: {error}')


@logger.catch
def dump_pickle(data, path):
    """Write data as pickle file"""
    with open(path, 'wb') as file_object:
        pickle.dump(data, file_object)
    logger.debug(f'Write pickle file: {type(data)}, path: {path}')


@logger.catch
def load_pickle(path):
    """Load data fro pickle file"""
    logger.debug(f'Read pickle file, path: {path}')
    with open(path, 'rb') as file_object:
        data = pickle.load(file_object)
    return data


@logger.catch
def create_folder(folder_path):
    """Creates folder if not exists"""
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        logger.debug(f'Create folder: {folder_path}')
    else:
        logger.debug(f'Folder exists: {folder_path}')


@logger.catch
def copytree(src, dst, symlinks=False, ignore=None):
    """Copy files and folders recursive"""
    for item in os.listdir(src):
        src_file = os.path.join(src, item)
        dst_file = os.path.join(dst, item)
        if os.path.isdir(src_file):
            shutil.copytree(src_file, dst_file, symlinks, ignore)
        else:
            shutil.copy2(src_file, dst_file)
    logger.debug(f'Copy folder structure, src: {src}, dst: {dst}')


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded"""

    def __init__(self, *args, **kwargs):
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))


def time_bubble(func):
    """Wraps methods/functions in an execution time counting sphere"""

    def wrap_func(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.warning(f'Function {func.__name__!r:<30}: {(end - start):.4f}s')
        return result

    return wrap_func
