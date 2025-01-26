from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from pyqtgraph.examples.MatrixDisplayExample import main_window


class MaxtestPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.label = QLabel()
        self.label.setText("Maximaltest")

        # Text größer machen
        font = QFont("Arial", 15)  # Schriftart und Schriftgröße
        self.label.setFont(font)
        #Text ausrichten und einfügen
        layout.addWidget(self.label, 0, 1, alignment = Qt.AlignmentFlag.AlignCenter)

        #Button für richtiges Zeichen des N-Backtests
        self.correct_button = QPushButton('Correct',self)
        width = self.width()
        print(width)
        width = int (width * 0.5)
        self.correct_button.setFixedWidth(width)
        #self.correct_button.setFixedWidth(160)  # Breite überschreiben
        self.correct_button.setFixedHeight(50) # Höhe überschreiben
        layout.addWidget(self.correct_button, 2, 0, alignment = Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen



        #Button für falsches Zeichen des N-Backtests
        self.skip_button = QPushButton('Skip',self)
        self.skip_button.setFixedWidth(160)  # Breite überschreiben
        self.skip_button.setFixedHeight(50) # Höhe überschreiben
        layout.addWidget(self.skip_button, 2, 2, alignment = Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen



        #N-Backtest einfügen
        self.charForTest = QLabel()
        font_test = QFont("Arial", 80)
        self.charForTest.setFont(font_test)
        self.charForTest.setText("n")
        layout.addWidget(self.charForTest, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
        self.setWindowTitle('Maxtest Widget')



    def updateChar(self):
        self.charForTest.setText("G")
        print("geht")
        #self.charForTest.setText(char)








