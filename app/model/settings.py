import json
import os
from .constants import *


class SettingsModel:

    DEFAULT_SETTINGS = {
        "isDarkMode": False,
    }

    def __init__(self, callback):
        self.settings = self.load_settings()
        self.callback = callback

    def load_settings(self):
        """Load settings from the file, or create default settings if the file doesn't exist."""
        file_path = os.path.join(getAbsPath(FOLDER_PATH_SETTINGS), FILE_NAME_SETTINGS)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if not os.path.exists(file_path):
            self.save_settings(self.DEFAULT_SETTINGS)
            self.callback.message.emit(
                self.callback.Level.DEBUG, "Loading default settings"
            )
            return self.DEFAULT_SETTINGS

        # Checking for missing keys, or wrong types
        with open(file_path, "r") as file:
            settings = json.load(file)
            for key, value in self.DEFAULT_SETTINGS.items():
                if not (key in settings and isinstance(settings[key], type(value))):
                    self.callback.message.emit(
                        self.callback.Level.DEBUG,
                        f"Faulty key in settings: {key}, restoring to default",
                    )
                    self.save_settings(self.DEFAULT_SETTINGS)
                    return self.DEFAULT_SETTINGS
            return settings

    def set(self, updates):
        """Update and save settings.
        :param updates: A dictionary containing the updated settings
        """
        self.settings.update(updates)
        file_path = os.path.join(getAbsPath(FOLDER_PATH_SETTINGS), FILE_NAME_SETTINGS)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.callback.message.emit(self.callback.Level.DEBUG, "Saved Settings")

        with open(file_path, "w") as file:
            json.dump(self.settings, file, indent=4)

    @staticmethod
    def clear_sessions():
        dir_path = os.path.join(getAbsPath(HDF5_FOLDER_PATH))
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                os.remove(file_path)
