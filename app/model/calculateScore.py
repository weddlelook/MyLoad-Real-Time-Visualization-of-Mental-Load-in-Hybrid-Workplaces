from PyQt6.QtCore import pyqtSignal, QObject


class calculateScore(QObject):
    score = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.maxScore = 1
        self.baselineScore = 0






    def setMaxScore(self, maxScore):
        self.maxScore = maxScore



    def setBaselineScore(self, baselineScore):
        self.baselineScore = baselineScore


    def calculatingScore(self, powers):

        self.currentindex = 0

        self.currentindex = powers['cognitive_load']
        print("theta")
        print(powers['theta_power'])
        print("alpha")
        print(powers['alpha_power'])
        print( "cogloadindex")
        print(self.currentindex)

        score = 10 + (self.currentindex - self.baselineScore) / (self.maxScore - self.baselineScore) * 80
        print(score)
        if score < 0:
            score = 0
        elif score > 100:
            score = 100
        print("Score")
        print(score)
        self.score.emit(int(score))





















