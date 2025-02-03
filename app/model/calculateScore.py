

class CalculateScore:

    def __init__(self):
        self.maxScore = 0
        self.baselineScore = 0



    def setMaxScore(self, maxScore):
        self.maxScore = maxScore



    def setBaselineScore(self, baselineScore):
        self.baselineScore = baselineScore


    def calculateScore(self, currentScore):
        scorePercentage = 10 + (currentScore - self.baselineScore) / (self.maxScore - self.baselineScore) * 80

        if scorePercentage < 0:
            scorePercentage = 0
        elif scorePercentage > 100:
            scorePercentage = 100


        return scorePercentage





















