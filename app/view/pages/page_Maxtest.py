from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont



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

        #Horizontal Layout for the buttons
        h_layout = QHBoxLayout()
        #Button für richtiges Zeichen des N-Backtests
        self.correct_button = QPushButton('Correct')
        h_layout.addWidget(self.correct_button, alignment=Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen
        #Button für falsches Zeichen des N-Backtests
        self.skip_button = QPushButton('Skip')
        h_layout.addWidget(self.skip_button, alignment = Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen
        self.correct_button.hide()

        layout.addLayout(h_layout)
        self.setLayout(layout)
        self.setWindowTitle('Maxtest Widget')

    def updateChar(self, testChar):
        self.charForTest.setText(testChar)

    def show_correct_button(self):
        self.correct_button.show()







