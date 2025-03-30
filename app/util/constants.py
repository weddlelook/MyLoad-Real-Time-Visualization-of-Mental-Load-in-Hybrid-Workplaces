import os
import sys
from pathlib import Path

HDF5_FOLDER_PATH = folder_path = "h5_session_files"
FOLDER_PATH_SETTINGS = "setting_files"
FILE_NAME_SETTINGS = "user_settings.json"

N_BACKTEST = 2  # N for N backtest number
N_BACKTEST_PROPABILITY = [
    70,
    30,
]  # Probability of generating a new character vs the one from N back
NUM_CHANNELS = 8
WINDOW_SIZE = 15
THRESHOLD_UPPER = 7.47

def getAbsPath(relative_path):
    bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    parent_dir = bundle_dir.parent  # Move to the parent of the script directory
    print(parent_dir/relative_path)
    return parent_dir / relative_path