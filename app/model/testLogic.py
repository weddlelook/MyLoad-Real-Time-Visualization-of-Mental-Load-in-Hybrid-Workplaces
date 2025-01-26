import random
import string

from PyQt6.QtCore import QTimer, pyqtSignal, QObject


class testLogic(QObject):

    charSubmiter = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.charList = []
        self.booleanList = []
        self.n = 2


    def startTest(self):
        self.test_timer = QTimer()
        self.test_timer.start(100000)
        #self.n = n


    def generateChar(self):
        if self.test_timer.isActive():
            testChar = random.choice(string.ascii_uppercase)
            if len(self.charList) >= self.n :
                nBackChar = self.charList[len(self.charList) - self.n]
                print(nBackChar)
                testChar = random.choices([testChar, nBackChar], [10, 90])[0]
                print(testChar)
            self.charList.append(testChar)
            self.charSubmiter.emit(testChar)

    def correctButtonClicked(self):
        self.booleanList.append(True)
        self.generateChar()


    def skipButtonClicked(self):
        self.booleanList.append(False)
        self.generateChar()