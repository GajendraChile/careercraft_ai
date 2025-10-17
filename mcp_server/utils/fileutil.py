import os
import shutil

def get_all_file_paths(directory):
    file_paths = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            abs_path = os.path.abspath(os.path.join(dirpath, f))
            file_paths.append(abs_path)
    return file_paths

def make_directory(directory, folder):
    os.mkdir(os.path.abspath(os.path.join(directory, folder)))

def remove_directory(directory, folder):
    shutil.rmtree(os.path.join(directory, folder))