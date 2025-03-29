import os
import sys

FILE_PATH_CSS_LIGHTMODE = "styles/style_light.qss"

FILE_PATH_CSS_DARKMODE = "styles/style_dark.qss"

FILE_PATH_SETTINGS_ICON = "styles/images/settings-icon.png"

FILE_PATH_FONT = "styles/fonts/Lexend-VariableFont_wght.ttf"

FILE_PATH_INFO_ICON = "styles/images/info.png"

FILE_PATH_JITSI_HTML = "styles/jitsi.html"

FILE_PATH_OPEN_EYE_ICON = "styles/images/visual.png"

FILE_PATH_CLOSED_EYE_ICON = "styles/images/hidden_eye.png"

JITSI_PAGE_INFO = f"""The score displayed represents your Cognitive Load (CL) score. {os.linesep}
It is calculated using various values recorded by the headphones {os.linesep}
and processed through a formula to standardize it, allowing for {os.linesep}
comparison with your previous sessions."""


def getAbsPath(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    path_to_dat = os.path.abspath(os.path.join(bundle_dir, relative_path))
    return path_to_dat
