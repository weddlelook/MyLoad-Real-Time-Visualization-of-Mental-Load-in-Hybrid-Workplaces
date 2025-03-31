from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt


class ResultsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Your Result:")
        self.title_label.setObjectName("title")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        self.resultDisplay = QLabel()
        self.resultDisplay.setObjectName("subtitle")
        self.resultDisplay.setWordWrap(True)
        self.resultDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.resultDisplay)

        self.next_button = QPushButton("Next Page")
        layout.addWidget(
            self.next_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(layout)
        self.setWindowTitle("Results Widget")

    # This function updates the display of the result and writes how much was done correctly in the Maxtest.
    # This function is used in the controller after the test is finished.
    def updateResult(self, results):
        self.resultDisplay.setText(
            "You did " + str(results[0]) + " correct out of " + str(results[1])
        )
