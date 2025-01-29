from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
import sys

class StartWidget(QWidget):
    session_name_entered = pyqtSignal(str)  # Signal, um den Sessionnamen weiterzugeben

    def __init__(self):
        super().__init__()
        self.initUI()
        self.session_name = "tttt"

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 30, 20, 20)

        self.label = QLabel("Bitte geben Sie den Namen für die Session ein:", self)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.session_input = QLineEdit(self)
        self.session_input.setPlaceholderText('Session Name...')
        layout.addWidget(self.session_input, alignment=Qt.AlignmentFlag.AlignCenter)

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

        self.start_session_button = QPushButton('▶ Start a Session')
        layout.addWidget(self.start_session_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('Start Widget')

        self.start_session_button.clicked.connect(self._emit_session_name)

    def _emit_session_name(self):
        self.session_name = self.session_input.text().strip()
        if self.session_name:
            self.session_name_entered.emit(self.session_name)  # Signal mit dem eingegebenen Sessionnamen senden
        else:
            self.label.setText("Sessionname darf nicht leer sein!")  # Fehlerhinweis anzeigen

