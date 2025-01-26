import random
import string

from PyQt6.QtCore import QTimer, pyqtSignal, QObject


class testLogic(QObject):

    charSubmiter = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.charList = []
        self.booleanList = []


    def startTest(self, n):
        self.test_timer = QTimer()
        self.test_timer.start(300000)

        while(self.test_timer.isActive()):
            if len(self.charList) == len(self.booleanList):
                testChar = self.generateChar(n)
                self.charSubmiter.emit(testChar)


    def generateChar(self, n):
        testChar = random.choice(string.ascii_uppercase)
        if len(self.charList) > n :
            nBackChar = self.charList.index(len(self.charList) - 1 - n)
            testChar = random.choices([testChar, nBackChar], [80, 20])[0]
            self.charList.append(testChar)
        return testChar

    def correctButtonClicked(self):
        self.booleanList.append(True)

    def skipButtonClicked(self):
        self.booleanList.append(False)