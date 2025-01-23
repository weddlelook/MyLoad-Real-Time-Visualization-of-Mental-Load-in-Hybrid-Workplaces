from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
import sys

class StartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.monitor_start_button = QPushButton('startMonitoring', self)

        layout.addWidget(self.monitor_start_button)

        self.setLayout(layout)
        self.setWindowTitle('Start Widget')

        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Green background */
                color: white;              /* White text */
                border: 2px solid #4CAF50; /* Green border */
                border-radius: 10px;       /* Rounded corners */
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #3e8e41; /* Even darker green when pressed */
            }
        """)