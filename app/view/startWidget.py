from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLineEdit, QLabel
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

        self.monitor_start_button = QPushButton('startMonitoring', self)
        layout.addWidget(self.monitor_start_button, alignment= Qt.AlignmentFlag.AlignCenter)



        self.settings_button = QPushButton('Settings', self)
        layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.setWindowTitle('Start Widget')

        self.monitor_start_button.clicked.connect(self._emit_session_name)

        self.setStyleSheet("""
                    QPushButton {
                        background-color: #F4F4F4;  /* grey-ish background */
                        color: black;              /* black text */
                        border: 2px solid #000000; /* black border */
                        border-radius: 10px;       /* Rounded corners */
                        padding: 10px;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #D3D3D3; /* Darker grey on hover */
                    }
                    QPushButton:pressed {
                        background-color: #BEBEBE; /* Even darker grey when pressed */
                    }

                    QLabel {
                        font-size: 16px;
                        color: black;
                    }
                QLineEdit {
                background-color: #F4F4F4;   /* Helles Grau als Hintergrund */
                border: 2px solid #000000;    /* Schwarzer Rand */
                border-radius: 10px;          /* Abgerundete Ecken */
                padding: 5px;                 /* Innenabstand */
                font-size: 16px;              /* Schriftgröße */
                }

                QLineEdit:focus {
                    border: 2px solid #4CAF50;   /* Grüner Rand bei Fokus */
                    background-color: #ffffff;   /* Weißer Hintergrund bei Fokus */
                }

                QLineEdit::placeholder {
                    color: #888888;               /* Heller Grauton für Platzhaltertext */
                }

                """)
        self.monitor_start_button.setFixedWidth(200)  # Override the width in code

    def _emit_session_name(self):
        self.session_name = self.session_input.text().strip()
        if self.session_name:
            self.session_name_entered.emit(self.session_name)  # Signal mit dem eingegebenen Sessionnamen senden
        else:
            self.label.setText("Sessionname darf nicht leer sein!")  # Fehlerhinweis anzeigen

