from PyQt6.QtCore import QObject
import numpy as np
from app.util import Logger


class ScoreCalculator(QObject):

    def __init__(self, I_base, I_max, logger: Logger):
        super().__init__()
        self.logger = logger
        self.I_base = I_base
        self.I_max = I_max
        self.k, self.I_0 = self._solve_parameters()
        self.logger.message.emit(
            Logger.Level.DEBUG,
            f"Instantiated ScoreCalculator with parameter k = {self.k} and I_0 = {self.I_0}",
        )

    def _solve_parameters(self):
        """Solves for logistic function parameters k and I_0."""
        S_base, S_max = 10, 90
        logit_base = np.log(S_base / (100 - S_base))
        logit_max = np.log(S_max / (100 - S_max))

        k = (logit_max - logit_base) / (self.I_max - self.I_base)
        I_0 = self.I_base - logit_base / k
        return k, I_0

    def calculate_score(self, load_index: float) -> int:
        """Calculates the CL-Score from the given index
        :param load_index: The load_index to calculate from
        :return: calculated score as an Integer"""
        current_index = load_index if load_index else 0
        CLScore = 100 / (1 + np.exp(-self.k * (current_index - self.I_0)))
        return int(CLScore)
