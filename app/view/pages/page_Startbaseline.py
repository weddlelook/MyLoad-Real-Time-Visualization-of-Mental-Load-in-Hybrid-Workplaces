from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QLabel,
    QDialog,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap
import sys
from ..constants import *


class SkipDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.userUI()

    def userUI(self):

        self.setWindowTitle("Skip Confirmation")
        self.setFixedSize(600, 250)

        layout = QVBoxLayout()

        self.label = QLabel(
            "Are you sure you want to skip the test? "
            "Click skip if only you have already saved a session "
            "in which your conditions like sleep, time, etc are similar"
        )
        self.label.setObjectName("paragraph")
        self.label.setWordWrap(True)
        layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()

        self.no_button = QPushButton("No")
        self.no_button.clicked.connect(self.close)

        self.yes_button = QPushButton("Yes")
        self.yes_button.clicked.connect(self.close)

        button_layout.addWidget(self.no_button)
        button_layout.addWidget(self.yes_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


class StartBaselinePage(QWidget):
    def __init__(self):
        super().__init__()
        self.dialog = SkipDialog(self)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Before starting first...")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        explanation_label = QLabel(
            "Before starting monitoring your cognitive load we have to determine the your baseline. "
            "Close your eyes for a minute until you hear the bip and relax yourself. "
            'Please press "Start Measuring Baseline" to proceed. '
        )
        explanation_label.setObjectName("text")
        explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)

        self.monitor_baseline_button = QPushButton("Start Measuring Baseline", self)
        layout.addWidget(
            self.monitor_baseline_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Skip Button
        self.skipMaxtestButton = QPushButton("Skip")
        layout.addWidget(self.skipMaxtestButton, alignment=Qt.AlignmentFlag.AlignCenter)
        self.skipMaxtestButton.clicked.connect(self.dialog.exec)

        self.setLayout(layout)
        self.setWindowTitle("Start Baseline")

    @staticmethod
    def play_bip():
        delay_ms = 250
        QTimer.singleShot(delay_ms, lambda: QApplication.beep())
