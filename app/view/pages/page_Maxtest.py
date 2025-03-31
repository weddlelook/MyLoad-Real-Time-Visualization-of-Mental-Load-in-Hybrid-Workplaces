from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt


class MaxtestPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Test will end automatically when the timer runs out")
        self.title_label.setWordWrap(True)
        self.title_label.setObjectName("subtitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Display the letters
        self.charForTest = QLabel()
        self.charForTest.setObjectName("title")
        self.charForTest.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.charForTest)

        # Horizontal Layout for the buttons
        h_layout = QHBoxLayout()
        # Correct button for n back test
        self.correct_button = QPushButton("Correct")
        h_layout.addWidget(
            self.correct_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # skip button for n back test
        self.skip_button = QPushButton("Skip")
        h_layout.addWidget(
            self.skip_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addLayout(h_layout)
        self.setLayout(layout)
        self.setWindowTitle("Maxtest Widget")

    def updateChar(self, testChar):
        self.charForTest.setText(testChar)

    def show_correct_button(self):
        self.correct_button.show()

    def hide_correct_button(self):
        self.correct_button.hide()
