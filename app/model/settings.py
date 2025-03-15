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

        folder_path = getAbsPath(FOLDER_PATH_SETTINGS)
        file_path = os.path.join(folder_path, FILE_NAME_SETTINGS)

        os.makedirs(folder_path, exist_ok=True)

        if not os.path.exists(file_path):
            self.create_settings()

        with open(file_path, 'r') as file:
            return json.load(file)


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

    def create_settings(self):
        """Creates a new settings file from default settings"""
        folder_path = getAbsPath(FOLDER_PATH_SETTINGS)
        file_path = os.path.join(folder_path, FILE_NAME_SETTINGS)
        default_settings = SettingsModel.DEFAULT_SETTINGS

        with open(file_path, 'w') as file:
            json.dump(default_settings, file, indent=4)

    @staticmethod
    def clear_sessions():
        dir_path = os.path.join(getAbsPath(HDF5_FOLDER_PATH))
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                os.remove(file_path)
