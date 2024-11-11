import os
import shutil


def remove_path_if_exist(file_path):
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)


def create_dir_if_not_exist(filepath):
    if os.path.exists(filepath) and os.path.isdir(filepath):
        return
    else:
        os.mkdir(filepath)