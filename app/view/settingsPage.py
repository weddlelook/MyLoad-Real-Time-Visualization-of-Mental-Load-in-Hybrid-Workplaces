from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QFormLayout, QRadioButton
from PyQt6.QtCore import pyqtSignal
from app.model.settings import SettingsModel


class SettingsWidget(QWidget):
    settings_changed = pyqtSignal(dict)
    go_back = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create form layout for settings
        form_layout = QFormLayout()

        # Create widgets for settings
        self.traffic_light_option = QRadioButton("Traffic Light")
        self.bar_option = QRadioButton("Bar")


        form_layout.addRow('', self.traffic_light_option)
        form_layout.addRow('', self.bar_option)

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
            dic["bar"] = 1
            dic["trafficLight"] = 0
        self.settings_changed.emit(dic)
        self.go_back.emit()


    def set_settings(self, settings):
        self.settings = settings
        if self.settings.get("trafficLight") == 1:
            self.traffic_light_option.setChecked(True)
        elif self.settings.get("bar") == 1:
            self.bar_option.setChecked(True)

