from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import sys

class BaselineWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setText("Baseline is being measured")

        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setWindowTitle('Baseline Widget')

        