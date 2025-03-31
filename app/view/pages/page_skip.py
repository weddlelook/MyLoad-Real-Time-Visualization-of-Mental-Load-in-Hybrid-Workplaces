from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime, timedelta
import os
from app.util import HDF5_FOLDER_PATH, getAbsPath


class SkipPageWidget(QWidget):
    sessionSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.session_folder = getAbsPath(HDF5_FOLDER_PATH)
        self.initUI()
        self.selected_items = None

    def initUI(self):
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        label = QLabel(
            "To proceed, choose a session from your recorded sessions of the last two days"
            " that has similar conditions, such as sleep, energy, and other"
            " factors, to this session."
        )
        label.setWordWrap(True)
        label.setObjectName("subtitle")
        v_layout.addWidget(label, Qt.AlignmentFlag.AlignLeft)

        self.session_list = QListWidget()
        self.session_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.session_list.itemSelectionChanged.connect(self.update_next_button)
        v_layout.addWidget(self.session_list)

        self.back_button = QPushButton("Go Back")
        h_layout.addWidget(self.back_button, Qt.AlignmentFlag.AlignCenter)

        self.next_button = QPushButton("Choose Session")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.on_next_button_clicked)
        h_layout.addWidget(self.next_button, Qt.AlignmentFlag.AlignCenter)
        v_layout.addLayout(h_layout)
        self.load_sessions()

        self.setLayout(v_layout)

    def update_next_button(self):
        # Enable only if an item is selected
        if self.session_list.selectedItems():
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

    def load_sessions(self):
        """Load the h5 session files"""
        self.session_list.clear()
        if os.path.exists(self.session_folder):
            files = [f for f in os.listdir(self.session_folder) if f.endswith(".h5")]

            def extract_index(file_name):
                file_name = str(file_name)
                index = file_name.split("__")[0].strip()
                return int(index)

            def extract_date(file_name):
                # Extract the date part from the filename
                date_str = file_name.split("__")[2].split("_")[1].split(".")[0].strip()
                # Convert the date string to a datetime object
                return datetime.strptime(date_str, "%d-%m-%Y")

            current_date = datetime.now()
            two_days_ago = current_date - timedelta(days=2)

            # Filter files that are not older than two weeks
            recent_files = [f for f in files if extract_date(f) >= two_days_ago]

            # Sort the files by index in reverse order
            recent_files.sort(key=extract_index, reverse=True)
            # Skips the just made session in the listing
            recent_files = recent_files[1:]
            for file in recent_files:
                self.session_list.addItem(file)

    def on_next_button_clicked(self):
        self.selected_items = self.session_list.selectedItems()
        if self.selected_items:
            self.selected_file = self.selected_items[0].text()
            self.sessionSelected.emit(self.selected_file)
