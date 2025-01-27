from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
import sys

class StartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.monitor_start_button = QPushButton('startMonitoring', self)
        layout.addWidget(self.monitor_start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.settings_button = QPushButton('Settings', self)
        layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.setWindowTitle('Start Widget')


        self.monitor_start_button.setFixedWidth(200)  # Override the width in code
