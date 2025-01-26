from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys

class BaselineWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setText("Baseline is being measured")

        # Text zentrieren
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Text größer machen
        font = QFont("Arial", 15)  # Schriftart und Schriftgröße
        self.label.setFont(font)

        # Optional: Weitere Text-Styles mit StyleSheet
        self.label.setStyleSheet("color: #333;")  # Textfarbe ändern

        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setWindowTitle('Baseline Widget')
