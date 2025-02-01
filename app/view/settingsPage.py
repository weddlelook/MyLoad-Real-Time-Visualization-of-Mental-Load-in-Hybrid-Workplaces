from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QFormLayout, QRadioButton, QButtonGroup, QGroupBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from app.model.settings import SettingsModel


class SettingsWidget(QWidget):
    new_settings = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        #Container for display seetings
        display_container = QGroupBox("Display Settings")
        display_layout = QVBoxLayout()
        display_label = QLabel("Change the display type")
        display_label.setObjectName("text-settings")

        #Buttons for display settings
        self.traffic_light_option = QRadioButton("Traffic Light")
        self.bar_option = QRadioButton("Bar")

        display_layout.addWidget(display_label)
        display_layout.addWidget(self.traffic_light_option)
        display_layout.addWidget(self.bar_option)

        #Grouping buttons so only one can be checked at same time
        self.display_options = QButtonGroup(self)
        self.display_options.addButton(self.traffic_light_option)
        self.display_options.addButton(self.bar_option)

        display_container.setLayout(display_layout)

        # Container for Mode Settings
        mode_container = QGroupBox("Mode Settings")
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Change the mode")
        mode_label.setObjectName("text-settings")

        #Mode settings buttons
        self.light_mode_option = QRadioButton("Light Mode")
        self.dark_mode_option = QRadioButton("Dark Mode")
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.light_mode_option)
        mode_layout.addWidget(self.dark_mode_option)

        #Grouping buttons so only one can be checked at same time
        self.mode_option = QButtonGroup(self)
        self.mode_option.addButton(self.light_mode_option)
        self.mode_option.addButton(self.dark_mode_option)

        mode_container.setLayout(mode_layout)

        form_layout.addRow(display_container)
        form_layout.addRow(mode_container)
        layout.addLayout(form_layout)

        #Layout for buttons
        horizontal_layout = QHBoxLayout()
        # Back button
        self.back_button = QPushButton('Back')
        horizontal_layout.addWidget(self.back_button)

        # Save button
        self.save_button = QPushButton('Save Changes')
        horizontal_layout.addWidget(self.save_button)

        layout.addLayout(horizontal_layout)

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

