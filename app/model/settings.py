import json
import os
from .constants import *


class SettingsModel:

    DEFAULT_SETTINGS = {
        'isDarkMode': False,
        'showDisplay': True,
    }
    def __init__(self):
        self.settings = self.load_settings()


    def load_settings(self):
        """Load settings from the file, or return default settings if file doesn't exist."""
        settings_exist = False
        folder_path = getAbsPath(FOLDER_PATH_SETTINGS)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path, FILE_NAME_SETTINGS)
            if os.path.exists(file_path):
                settings_exist = True
        if settings_exist:
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            # Default settings if no settings file exists
            return SettingsModel.DEFAULT_SETTINGS

    def save_settings(self):
        """Save the current settings to the settings file."""
        folder_path = getAbsPath(FOLDER_PATH_SETTINGS)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, FILE_NAME_SETTINGS)
        with open(file_path, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def set(self, dic):
        for key, value in dic.items():
            self.settings[key] = value
        self.save_settings()

    @staticmethod
    def clear_sessions():
        dir_path = os.path.join(getAbsPath(HDF5_FOLDER_PATH))
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                os.remove(file_path)
