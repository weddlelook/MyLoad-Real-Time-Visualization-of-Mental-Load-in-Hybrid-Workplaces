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

        title_label = QLabel()
        title_label.setText("Baseline is being measured")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)

        self.setLayout(layout)
        self.setWindowTitle('Baseline Widget')
