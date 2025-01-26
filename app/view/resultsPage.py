from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ResultsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        layout = QGridLayout()

        self.label = QLabel()
        self.label.setText("Ihre Ergebnisse:")

        # Text größer machen
        font = QFont("Arial", 15)  # Schriftart und Schriftgröße
        self.label.setFont(font)
        # Text ausrichten und einfügen
        layout.addWidget(self.label, 0, 1, alignment = Qt.AlignmentFlag.AlignCenter)

        # Button um zur nächsten Seite zu kommen
        self.next_button = QPushButton('Next Page')
        layout.addWidget(self.next_button, 2, 2, alignment = Qt.AlignmentFlag.AlignCenter)  # Button ausrichten und einfügen

        self.resultDisplay = QLabel()
        font_test = QFont("Arial", 30)
        self.resultDisplay.setFont(font_test)
        self.resultDisplay.setText("")
        layout.addWidget(self.resultDisplay, 1, 1, alignment = Qt.AlignmentFlag.AlignHCenter)



    def updateResult(self, results):
        self.resultDisplay.setText("Sie haben " + results[0] + " von " + results[1] + results[0] + " richtig gemacht.")


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Calculate 10% width and 15% height of the parent widget
        button_width = int(self.width() * 0.1)
        button_height = int(self.height() * 0.15)

        # Set button sizes dynamically
        self.next_button.setFixedSize(button_width, button_height)