from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
import sys

class StartBaselinePage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel('Before starting first...')
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        explanation_label = QLabel(
            'Before starting monitoring your cognitive load we have to determine the your baseline. '
            'Close your eyes for a minute until you hear the bip and relax yourself. '
            'Please press "Start Measuring Baseline" to proceed. '
        )
        explanation_label.setObjectName("text")
        explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)

        self.monitor_baseline_button = QPushButton('Start Measuring Baseline', self)
        layout.addWidget(self.monitor_baseline_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('Start Baseline')

