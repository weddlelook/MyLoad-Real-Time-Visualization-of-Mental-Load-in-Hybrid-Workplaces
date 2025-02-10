from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

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
        # Text ausrichten und einfügen
        layout.addWidget(self.title_label)

        # Erstellt den Text für das Ergeniss
        self.resultDisplay = QLabel()
        self.resultDisplay.setObjectName("subtitle")
        self.resultDisplay.setWordWrap(True)
        self.resultDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.resultDisplay)

        # Button um zur nächsten Seite zu kommen
        self.next_button = QPushButton('Next Page')
        layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Button ausrichten und einfügen

        self.setLayout(layout)
        self.setWindowTitle('Results Widget')

    # Diese Funktion updatet das Display des Ergebnisses und schreibt dort hin wie viel im Maxtest richtig gemacht wurde
    # Diese Funktion wird im Controller benutzt nachdem der Test fertig ist
    def updateResult(self, results):
        self.resultDisplay.setText("You did " + str(results[0]) + " correct out of " + str(results[1] + results[0]))
