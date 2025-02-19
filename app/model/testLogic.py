import random
import string

from PyQt6.QtCore import QTimer, pyqtSignal, QObject


class testLogic(QObject):

    charSubmiter = pyqtSignal(str)
    showButton = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.charList = []
        self.booleanList = []
        self.n = 3  # N ist N backtest Zahl wenn später durch funktion übergeben hier einfach dann gleich 0 eingeben

        """
        Dat Problem war, dass du den schon connected hast bevor du 
        den überhaupt instanziiert hast,
        Die Aufrufe mit test_timer.timeout.connect sind also quasi auf nem noch
        nicht vorhandenen Objekt passiert das du startTest erst nach denen aufgerufen hast
        Warum das da noch nicht gemeckert hat ist fraglich.
        """
        self.test_timer = QTimer()
        self.test_timer.setSingleShot(True)

    # Funktion zum Start des Maxtest und des Timers für diesen
    # Wird im Controller aufgerufen sobald der Baseline Test fertig istw
    # Hier könnte dann auch noch eine Zahl übergeben werden n falls verschiedene n Backtest gemacht werden sollen
    def startTest(self):
        self.test_timer.start(10000)
        self.generateChar()
        #self.n = n


    # Funktion generiert einen zufälligen Buchstaben und verändert dann die Wahrscheinlichkeit falls es einen Buchstaben
    # n Stellen davor gibt
    # Die Wahrscheinlichkeit wird durch random choiche verändert mit den weight
    def generateChar(self):
        #if self.test_timer.isActive():
        if True :
            testChar = random.choice(string.ascii_uppercase)
            if len(self.charList) >= self.n :
                nBackChar = self.charList[len(self.charList) - self.n]
                testChar = random.choices([testChar, nBackChar], [70, 30])[0]
            self.charList.append(testChar)
            self.charSubmiter.emit(testChar)


    #Funktion wird aufgerufen wenn der Correct Button auf der Maxtest seite aufgerufen und hängt dann an die booleanList
    # ein True um den gedrückten Button zu speichern
    #Außerdem ruft es generateChar auf um einen neuen Code zu erstellen
    def correctButtonClicked(self):
        self.booleanList.append(True)
        self.generateChar()

    # Funktion wird aufgerufen wenn der Skip Button auf der Maxtest seite aufgerufen und hängt dann an die booleanList
    # ein False um den gedrückten Button zu speichern
    # Außerdem ruft es generateChar auf um einen neuen Code zu erstellen
    def skipButtonClicked(self):
        self.booleanList.append(False)
        self.generateChar()
        if len(self.booleanList) == self.n :
            self.showButton.emit()



    # Diese Funktion berechnet aus der Liste der Buchstaben und der Liste der booleans also welcher Knopf gedrückt wurde
    # wie oft die Person das richtige geklickt hat
    # Wird im COntroller der ResultsPage aufgerufen
    def calculateResults(self):
        result = [0, 0]
        i = 0
        while i < len(self.charList) - 1:
            if i < self.n:
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


