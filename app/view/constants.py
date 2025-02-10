FILE_PATH_CSS_LIGHTMODE = "app/view/styles/style_light.qss"

FILE_PATH_CSS_DARKMODE = "app/view/styles/style_dark.qss"

FILE_PATH_SETTINGS_ICON = "app/view/styles/images/settings-icon.png"

FILE_PATH_FONT = "app/view/styles/fonts/Lexend-VariableFont_wght.ttf"

FILE_PATH_INFO_ICON = "styles/images/info.png"

FILE_PATH_JITSI_HTML = "styles/jitsi.html"

import os

def getAbsPath(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))