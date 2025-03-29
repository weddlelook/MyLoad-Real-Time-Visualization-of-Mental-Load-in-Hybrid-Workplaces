from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QApplication,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
)
from PyQt6.QtCore import Qt, QSize, QDir, pyqtSignal
from setuptools.warnings import InformationOnly
import os
from ..constants import *


class StartMaxTestPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        v_layout = QVBoxLayout()

        self.title_label = QLabel("Now we test your maximal cognitive load!")
        self.title_label.setObjectName("title")
        v_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.explanation_label = QLabel(
            "You will see a series of letters, one at a time. "
            "Your task is to compare each letter with the one that appeared exactly 2 steps earlier. "
            "If the current letter matches the letter from 2 steps ago, click Correct else Skip."
        )
        self.explanation_label.setObjectName("text")
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.addWidget(self.explanation_label)

        self.ready_label = QLabel("Are you ready?")
        self.ready_label.setObjectName("subtitle")
        v_layout.addWidget(self.ready_label, alignment=Qt.AlignmentFlag.AlignCenter)

        h_layout = QHBoxLayout()
        # Start Button
        self.startMaxtestButton = QPushButton("Start")
        h_layout.addWidget(
            self.startMaxtestButton, alignment=Qt.AlignmentFlag.AlignCenter
        )  # Button ausrichten und einfügen
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
        self.setWindowTitle("StartMaxtest Widget")
