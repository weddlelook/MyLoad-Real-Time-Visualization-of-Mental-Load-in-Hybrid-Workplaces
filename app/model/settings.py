import json
import os


class SettingsModel:

    FOLDER_PATH = os.path.join(os.path.dirname(__file__), '../Settings Files')
    FILE_NAME = 'user_settings.json'
    DEFAULT_SETTINGS = {
        'trafficLight': 1,
        'bar': 0,
        'lightMode': 1,
        'darkMode': 0,
    }
    print(DEFAULT_SETTINGS)
    def __init__(self):
        self.settings = self.load_settings()


    def load_settings(self):
        """Load settings from the file, or return default settings if file doesn't exist."""
        if os.path.exists(SettingsModel.FOLDER_PATH):
            file_path = os.path.join(SettingsModel.FOLDER_PATH, SettingsModel.FILE_NAME)
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            # Default settings if no settings file exists
            return SettingsModel.DEFAULT_SETTINGS

    def save_settings(self):
        """Save the current settings to the settings file."""
        if not os.path.exists(SettingsModel.FOLDER_PATH):
            os.makedirs(SettingsModel.FOLDER_PATH)
        file_path = os.path.join(SettingsModel.FOLDER_PATH, SettingsModel.FILE_NAME)
        with open(file_path, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def set(self, dic):
        for key, value in dic.items():
            self.settings[key] = value
        self.save_settings()