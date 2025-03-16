from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton, \
    QMessageBox, QVBoxLayout, QHBoxLayout, QDialog, QListWidget
from PyQt6.QtCore import Qt, QSize, QDir, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
from setuptools.warnings import InformationOnly
import os
from ..constants import *


class SkipPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        self.session_list = QListWidget()
        self.session_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.session_list.itemSelectionChanged.connect(self.update_next_button)
        v_layout.addWidget(self.session_list)

        self.back_button = QPushButton("Go Back")
        h_layout.addWidget(self.back_button, Qt.AlignmentFlag.AlignCenter)

        self.next_button = QPushButton("Choose Session")
        self.next_button.setEnabled(False)
        h_layout.addWidget(self.next_button, Qt.AlignmentFlag.AlignCenter)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

    def update_next_button(self):
        # Enable only if an item is selected
        if self.session_list.selectedItems():
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

    def load_sessions(self):
        """Lade alle .h5-Dateien aus dem Session-Ordner."""
        self.session_list.clear()
        if os.path.exists(self.session_folder):
            files = [f for f in os.listdir(self.session_folder) if f.endswith(".h5")]

            def extract_index(file_name):
                file_name = str(file_name)
                index = file_name.split("__")[0].strip()
                return int(index)

            files.sort(key=extract_index, reverse=True)
            for file in files:
                self.session_list.addItem(file)