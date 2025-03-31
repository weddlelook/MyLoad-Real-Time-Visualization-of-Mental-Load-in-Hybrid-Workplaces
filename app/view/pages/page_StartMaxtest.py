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
from app.util import MAXTEST_PAGE_INFO


class StartMaxTestPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        v_layout = QVBoxLayout()

        self.title_label = QLabel("Now we test your maximal cognitive load!")
        self.title_label.setObjectName("title")
        v_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.explanation_label = QLabel(MAXTEST_PAGE_INFO)
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
