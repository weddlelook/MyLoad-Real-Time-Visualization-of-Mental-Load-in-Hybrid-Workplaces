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

        self.setStyleSheet("""
            QPushButton {
                background-color: #F4F4F4;  /* grey-ish background */
                color: black;              /* black text */
                border: 2px solid #000000; /* black border */
                border-radius: 10px;       /* Rounded corners */
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #D3D3D3; /* Darker grey on hover */
            }
            QPushButton:pressed {
                background-color: #BEBEBE; /* Even darker grey when pressed */
            }
        """)
        self.monitor_start_button.setFixedWidth(200)  # Override the width in code
