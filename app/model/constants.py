import os
import sys

HDF5_FOLDER_PATH = folder_path = "../h5_session_files"
FOLDER_PATH_SETTINGS = "../Settings Files"
FILE_NAME_SETTINGS = "user_settings.json"

N_BACKTEST = 2  # N for N backtest number
N_BACKTEST_PROPABILITY = [
    70,
    30,
]  # Probability of generating a new character vs the one from N back


def getAbsPath(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    path_to_dat = os.path.abspath(os.path.join(bundle_dir, relative_path))
    return path_to_dat
