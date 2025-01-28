from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
import sys

class StartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Welcome to MyLoad")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        text_label = QLabel(
            "MyLoad provide users the opportunity to monitor their cognitive load during online lectures,"
            " helping them optimize focus, productivity, and overall performance."
        )
        text_label.setObjectName("text")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)
        layout.addWidget(text_label)

        self.start_session_button = QPushButton('Start a Session')
        layout.addWidget(self.start_session_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('Start Widget')


        self.start_session_button.setFixedWidth(200)  # Override the width in code
