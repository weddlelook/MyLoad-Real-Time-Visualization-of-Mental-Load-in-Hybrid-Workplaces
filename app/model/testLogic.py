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

        """
        Dat Problem war, dass du den schon connected hast bevor du 
        den überhaupt instanziiert hast,
        Die Aufrufe mit test_timer.timeout.connect sind also quasi auf nem noch
        nicht vorhandenen Objekt passiert das du startTest erst nach denen aufgerufen hast
        Warum das da noch nicht gemeckert hat ist fraglich.
        """
        self.test_timer = QTimer()
        self.test_timer.setSingleShot(True)


    def startTest(self):
        self.test_timer.start(10000)
        self.generateChar()
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

    def calculateResults(self):
        result = [0, 0]
        i = 0
        while i < len(self.charList) - 1:
            if i <= self.n:
                if self.booleanList[i] == False:
                    result[0] += 1
                else:
                    result[1] += 1
            else:
                if self.charList[i] == self.charList[i - self.n] and self.booleanList[i] == True:
                    result[0] += 1
                elif self.charList[i] != self.charList[i - self.n] and self.booleanList[i] == False:
                    result[0] += 1
                else:
                    result[1] += 1
            i += 1

        return result


