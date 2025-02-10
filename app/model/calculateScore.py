from PyQt6.QtCore import pyqtSignal, QObject


class calculateScore(QObject):
    score = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.maxScore = 8
        self.baselineScore = 2






    def setMaxScore(self, maxScore):
        self.maxScore = maxScore



    def setBaselineScore(self, baselineScore):
        self.baselineScore = baselineScore


    def calculatingScore(self, powers):

        self.currentScore = 0

        self.currentScore = powers['cognitive_load']
        print("theta")
        print(powers['theta_power'])
        print("alpha")
        print(powers['alpha_power'])
        print( "cogloadindex")
        print(self.currentScore)

        scorePercentage = 10 + (self.currentScore - self.baselineScore) / (self.maxScore - self.baselineScore) * 80
        print(scorePercentage)
        if scorePercentage < 0:
            scorePercentage = 0
        elif scorePercentage > 100:
            scorePercentage = 100
        print("Score")
        print(scorePercentage)
        self.score.emit(int(scorePercentage))





















