import os

HDF5_FOLDER_PATH = folder_path = '../h5_session_files'
FOLDER_PATH_SETTINGS = '../Settings Files'
FILE_NAME_SETTINGS = 'user_settings.json'


import os
import sys

def getAbsPath(relative_path):
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path_to_dat = os.path.abspath(os.path.join(bundle_dir, relative_path))
    return path_to_dat