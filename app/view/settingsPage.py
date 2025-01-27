from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QFormLayout, QRadioButton, QButtonGroup
from PyQt6.QtCore import pyqtSignal
from app.model.settings import SettingsModel


class SettingsWidget(QWidget):
    new_settings = pyqtSignal(dict)
    settings_changed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create form layout for settings
        form_layout = QFormLayout()

        # Create widgets for settings
        self.display_label = QLabel("Change the display type")
        self.traffic_light_option = QRadioButton()
        self.bar_option = QRadioButton()
        form_layout.addRow(self.display_label)
        form_layout.addRow('Traffic Light', self.traffic_light_option)
        form_layout.addRow("Bar", self.bar_option)

        self.display_options = QButtonGroup(self)
        self.display_options.addButton(self.traffic_light_option)
        self.display_options.addButton(self.bar_option)

        self.mode_label = QLabel("Change the mode")
        self.light_mode_option = QRadioButton()
        self.dark_mode_option = QRadioButton()
        form_layout.addRow(self.mode_label)
        form_layout.addRow("Light Mode", self.light_mode_option)
        form_layout.addRow("Dark Mode", self.dark_mode_option)

        self.mode_option = QButtonGroup(self)
        self.mode_option.addButton(self.light_mode_option)
        self.mode_option.addButton(self.dark_mode_option)

        layout.addLayout(form_layout)

        # Save button
        self.save_button = QPushButton('Save Changes')
        layout.addWidget(self.save_button)
        # Back button
        self.back_button = QPushButton('Back')
        layout.addWidget(self.back_button)

        self.save_button.clicked.connect(self.save_settings)
        self.setLayout(layout)
        self.setWindowTitle("Settings")

    def save_settings(self):
        dic = {}
        if self.traffic_light_option.isChecked():
            dic["trafficLight"] = 1
            dic["bar"] = 0
        elif self.bar_option.isChecked():
            dic["trafficLight"] = 0
            dic["bar"] = 1
        if self.light_mode_option.isChecked():
            dic["lightMode"] = 1
            dic["darkMode"] =0
        elif self.dark_mode_option.isChecked():
            dic["lightMode"] = 0
            dic["darkMode"] = 1
        self.new_settings.emit(dic)
        self.settings_changed.emit()

    def set_settings(self, settings):
        self.settings = settings
        if self.settings.get("trafficLight") == 1:
            self.traffic_light_option.setChecked(True)
        elif self.settings.get("bar") == 1:
            self.bar_option.setChecked(True)
        if self.settings.get("lightMode") == 1:
            self.light_mode_option.setChecked(True),
        elif self.settings.get("darkMode") == 1:
            self.dark_mode_option.setChecked(True)

