from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton, \
    QMessageBox, QVBoxLayout, QHBoxLayout, QDialog
from PyQt6.QtCore import Qt, QSize, QDir, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
from setuptools.warnings import InformationOnly
import os
from ..constants import *


class SkipDialog(QDialog):

    skipConfirmed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Skip Confirmation")
        self.setFixedSize(600, 250)

        layout = QVBoxLayout()

        self.label = QLabel("Are you sure you want to skip the test? "
                            "Click skip if only you have already saved a session "
                            "in which your conditions like sleep, time, etc are similar")
        self.label.setObjectName("paragraph")
        self.label.setWordWrap(True)
        layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()
        self.yes_button = QPushButton("Yes")
        self.yes_button.clicked.connect(self.confirm_skip)  

        self.no_button = QPushButton("No")
        self.no_button.clicked.connect(self.reject)  

        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def confirm_skip(self):
        self.skipConfirmed.emit()  
        self.accept()  


class StartMaxTestPage(QWidget):
    def __init__(self):
        super().__init__()
        self.dialog = SkipDialog(self)
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
        #Start Button
        self.startMaxtestButton = QPushButton("Start")
        h_layout.addWidget(self.startMaxtestButton, alignment=Qt.AlignmentFlag.AlignCenter)  # Button ausrichten und einfügen
        #Skip Button
        self.skipMaxtestButton = QPushButton("Skip")

        # Popup als Info zum skippen / Kann man sich überlegen das direkt auf den skip button zu machen
        # Hier Icon einfügen
        info_icon_path = getAbsPath(FILE_PATH_INFO_ICON)
        self.skipMaxtestButton.setIcon(QIcon(info_icon_path))
       # self.skipMaxtestButton.setToolTip("Click skip if only you have already saved a session "
        #                                  "in which your conditions like sleep, time, etc are similar")
        h_layout.addWidget(self.skipMaxtestButton, alignment=Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen

        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
        self.setWindowTitle('StartMaxtest Widget')

   
    def show_skip_dialog(self):
        self.dialog.exec() 