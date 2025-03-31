import os
import sys
from pathlib import Path
from .logger import Logger
import serial.tools.list_ports


LOGGER_LEVEL = (
    Logger.Level.DEBUG
)  # Level of console logging comments, available: INFO, DEBUG, ERROR

N_BACKTEST = 2  # N for N backtest number
N_BACKTEST_PROPABILITY = [
    70,
    30,
]  # Probability of generating a new character vs the one from N back
NUM_CHANNELS = 8
WINDOW_SIZE = 15
THRESHOLD_UPPER = 7.47

HDF5_FOLDER_PATH = Path("res") / "h5_session_files"
FOLDER_PATH_SETTINGS = Path("res") / "setting_files"
FILE_NAME_SETTINGS = Path("res") / "user_settings.json"

MAX_PHASE_LENGTH = 90000
MIN_PHASE_LENGTH = 60000

FILE_PATH_RES = Path("res")
FILE_PATH_CSS_LIGHTMODE = FILE_PATH_RES / "styles" / "style_light.qss"
FILE_PATH_CSS_DARKMODE = FILE_PATH_RES / "styles" / "style_dark.qss"
FILE_PATH_SETTINGS_ICON = FILE_PATH_RES / "styles" / "images" / "settings-icon.png"
FILE_PATH_FONT = FILE_PATH_RES / "styles" / "fonts" / "Lexend-VariableFont_wght.ttf"
FILE_PATH_INFO_ICON = FILE_PATH_RES / "styles" / "images" / "info.png"
FILE_PATH_JITSI_HTML = FILE_PATH_RES / "styles" / "jitsi.html"
FILE_PATH_OPEN_EYE_ICON = FILE_PATH_RES / "styles" / "images" / "visual.png"
FILE_PATH_CLOSED_EYE_ICON = FILE_PATH_RES / "styles" / "images" / "hidden_eye.png"
MAXTEST_PAGE_INFO = f"""You will see a series of letters, one at a time. {os.linesep}
Your task is to compare each letter with the one that appeared exactly {N_BACKTEST} steps earlier. {os.linesep}
If the current letter matches the letter from {N_BACKTEST} steps ago, click Correct else Skip. {os.linesep}"""

JITSI_PAGE_INFO = f"""The score displayed represents your Cognitive Load (CL) score. {os.linesep}
It is calculated using various values recorded by the headphones {os.linesep}
and processed through a formula to standardize it, allowing for {os.linesep}
comparison with your previous sessions."""


def getAbsPath(relative_path):
    bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    parent_dir = bundle_dir.parent  # Move to the parent of the script directory
    return parent_dir / relative_path


def find_usb_port():
    """Automatically finds an available USB serial port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "ttyUSB" in port.device or "COM" in port.device:
            return port.device  # Returns first detected USB port
    return None
