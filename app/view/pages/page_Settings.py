from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QFormLayout, QRadioButton, QButtonGroup, QGroupBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from app.model.settings import SettingsModel


class SettingsWidget(QWidget):
    new_settings = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

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

        form_layout.addRow(mode_container)

        del_files_container = QGroupBox("Clear Files")
        del_files_layout = QHBoxLayout()
        del_files_label = QLabel("To clear all previous sessions information:")
        del_files_label.setObjectName("text-settings")

        self.clear_all_button = QPushButton("Clear All")
        del_files_layout.addWidget(del_files_label)
        del_files_layout.addWidget(self.clear_all_button)
        del_files_container.setLayout(del_files_layout)

        form_layout.addRow(del_files_container)

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
        if self.light_mode_option.isChecked():
            dic["isDarkMode"] = False
        elif self.dark_mode_option.isChecked():
            dic["isDarkMode"] = True
        self.new_settings.emit(dic)

    def set_settings(self, settings):
        self.settings = settings
        if self.settings.get("isDarkMode") == False:
            self.light_mode_option.setChecked(True),
        elif self.settings.get("isDarkMode") == True:
            self.dark_mode_option.setChecked(True)

