import json
import os
from pathlib import Path
from app.util import FOLDER_PATH_SETTINGS, FILE_NAME_SETTINGS, HDF5_FOLDER_PATH, getAbsPath
from app.util import Logger


class SettingsModel:

    DEFAULT_SETTINGS = {
        "isDarkMode": False,
    }

    def __init__(self, logger: Logger):
        self.logger = logger
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from the file, or create default settings if the file doesn't exist."""
        folder_path = getAbsPath(FOLDER_PATH_SETTINGS)
        file_path = folder_path / FILE_NAME_SETTINGS

        folder_path.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

        if not file_path.exists():
            self.set(self.DEFAULT_SETTINGS)
            self.logger.message.emit(
                self.logger.Level.DEBUG, "Loading default settings"
            )
            return self.DEFAULT_SETTINGS

        # Checking for missing keys, or wrong types
        with file_path.open("r") as file:
            settings = json.load(file)
            for key, value in self.DEFAULT_SETTINGS.items():
                if not (key in settings and isinstance(settings[key], type(value))):
                    self.logger.message.emit(
                        self.logger.Level.DEBUG,
                        f"Faulty key in settings: {key}, restoring to default",
                    )
                    self.save_settings(self.DEFAULT_SETTINGS)
                    return self.DEFAULT_SETTINGS
            return settings

    def set(self, updates):
        """Update and save settings.
        :param updates: A dictionary containing the updated settings
        """
        file_path = getAbsPath(FOLDER_PATH_SETTINGS) / FILE_NAME_SETTINGS
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directory exists

        with file_path.open("w") as file:
            json.dump(updates, file, indent=4)

        self.logger.message.emit(self.logger.Level.DEBUG, "Saved Settings")

    @staticmethod
    def clear_sessions():
        dir_path = os.path.join(getAbsPath(HDF5_FOLDER_PATH))
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                os.remove(file_path)
