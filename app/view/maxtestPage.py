from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont



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
        layout.addWidget(self.correct_button, 2, 0, alignment = Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen



        #Button für falsches Zeichen des N-Backtests
        self.skip_button = QPushButton('Skip',self)
        layout.addWidget(self.skip_button, 2, 2, alignment = Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen



        #N-Backtest einfügen
        self.charForTest = QLabel()
        font_test = QFont("Arial", 80)
        self.charForTest.setFont(font_test)
        self.charForTest.setText("n")
        layout.addWidget(self.charForTest, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
        self.setWindowTitle('Maxtest Widget')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Calculate 10% width and 15% height of the parent widget
        button_width = int(self.width() * 0.1)
        button_height = int(self.height() * 0.15)

        # Set button sizes dynamically
        self.correct_button.setFixedSize(button_width, button_height)
        self.skip_button.setFixedSize(button_width, button_height)

    def updateChar(self):
        self.charForTest.setText("G")
        print("geht")
        #self.charForTest.setText(char)








