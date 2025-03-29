from PyQt6.QtCore import pyqtSignal, QObject
import numpy as np

"""
We want to build a function for normalization of CLI values. Let name the function S. S should have the following features: 
S: I --> (0,100)
I = (0, ∞)
IBase, IMax ∈ I
S(IBase) ≈ 10
S(IMax) ≈ 90
lim I -> 0 S(I) = 0
lim I -> ∞ S(I) = 100
S is degressiv (? not decided on yet)

In the following there is the function logistic function, which fulfills the required features

"""


class calculateScore(QObject):
    score = pyqtSignal(int)

    def __init__(self, I_base, I_max):
        super().__init__()
        self.I_base = I_base
        self.I_max = I_max
        self.k, self.I_0 = self._solve_parameters()

    def _solve_parameters(self):
        """Solves for logistic function parameters k and I_0."""
        S_base, S_max = 10, 90  # Desired output mappings
        logit_base = np.log(S_base / (100 - S_base))
        logit_max = np.log(S_max / (100 - S_max))

        k = (logit_max - logit_base) / (self.I_max - self.I_base)
        I_0 = self.I_base - logit_base / k
        return k, I_0

    def calculatingScore(self, powers):

        self.currentIndex = 0

        print(self.I_base)
        print(self.I_max)
        self.currentIndex = powers["cognitive_load"]
        print("theta")
        print(powers["theta_power"])
        print("alpha")
        print(powers["alpha_power"])
        print("cogloadindex")
        print(self.currentIndex)

        CLScore = 100 / (1 + np.exp(-self.k * (self.currentIndex - self.I_0)))

        print("CLScore")
        print(CLScore)
        self.score.emit(int(CLScore))
        return int(CLScore)
