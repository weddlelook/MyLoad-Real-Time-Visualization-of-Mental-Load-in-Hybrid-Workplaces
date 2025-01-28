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
        self.label.setText("Ihr Ergebnisse:")

        # Text größer machen
        font = QFont("Arial", 15)  # Schriftart und Schriftgröße
        self.label.setFont(font)
        # Text ausrichten und einfügen
        layout.addWidget(self.label, 0, 1, alignment = Qt.AlignmentFlag.AlignCenter)

        # Button um zur nächsten Seite zu kommen
        self.next_button = QPushButton('Next Page')
        layout.addWidget(self.next_button, 2, 2, alignment = Qt.AlignmentFlag.AlignCenter)  # Button ausrichten und einfügen

        # Erstellt den Text für das Ergeniss
        self.resultDisplay = QLabel()
        font_test = QFont("Arial", 30) # verändert Schriftart und Schriftgröße
        self.resultDisplay.setFont(font_test)
        self.resultDisplay.setText("test")
        layout.addWidget(self.resultDisplay, 1, 1, alignment = Qt.AlignmentFlag.AlignHCenter) # Ausrichten

        self.setLayout(layout)
        self.setWindowTitle('Results Widget')


    # Diese Funktion updatet das Display des Ergebnisses und schreibt dort hin wie viel im Maxtest richtig gemacht wurde
    # Diese Funktion wird im Controller benutzt nachdem der Test fertig ist
    def updateResult(self, results):
        self.resultDisplay.setText("Sie haben " + str(results[0]) + " von " + str(results[1] + results[0]) + " richtig gemacht.")


    # Funktion verändert die Button größe automatisch mit größe des Windows
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Calculate 10% width and 15% height of the parent widget
        button_width = int(self.width() * 0.1)
        button_height = int(self.height() * 0.15)

        # Set button sizes dynamically
        self.next_button.setFixedSize(button_width, button_height)