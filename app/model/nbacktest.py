import random
import string

from PyQt6.QtCore import pyqtSignal, QObject
import app.util as const


class NBackTest(QObject):

    generated_char = pyqtSignal(str)
    show_correct_button = pyqtSignal()

    def __init__(self, callback):
        super().__init__()
        self.generated = None  # List of generated characters
        self.answer = None  # List of boolean values, true indicating the "correct" button was clicked
        self.callback = callback

    def start_test(self):
        """Start the test by initializing the lists and generating the first character."""
        self.generated = []
        self.answer = []
        self.generate_char()

    def generate_char(self):
        """Generate a new char and emit it via the signal."""
        try:
            random_char = random.choice(string.ascii_uppercase)
            char_to_send = random_char
            if len(self.generated) >= const.N_BACKTEST:
                back_n_char = self.generated[len(self.generated) - const.N_BACKTEST]
                char_to_send = random.choices(
                    [random_char, back_n_char], const.N_BACKTEST_PROPABILITY
                )[0]
            self.generated.append(char_to_send)
            self.generated_char.emit(char_to_send)
            self.callback.message.emit(
                self.callback.Level.DEBUG, f"Generated char: {char_to_send}"
            )
        except TypeError as e:
            self.callback.message.emit(
                self.callback.Level.ERROR,
                f"Error in generateChar: {e}, remember to start the test first.",
            )

    def submit_answer(self, answer: bool):
        """Adds the submitted answer to the list and emits a new char via the signal.
        :param answer: True if the "correct" button was clicked, False if skipped.
        """
        self.answer.append(answer)
        self.generate_char()
        if len(self.answer) == const.N_BACKTEST:
            self.show_correct_button.emit()
            self.callback.message.emit(self.callback.Level.DEBUG, "Show correct button")
        self.callback.message.emit(
            self.callback.Level.DEBUG, f"Answer submitted: {answer}"
        )

    def calculate_result(self):
        """Calculate the results of the test.
        :return: A tuple with the number of correct answers and the total number of questions.
        """
        correct_answers = 0
        if len(self.generated) <= const.N_BACKTEST:
            return (0, 0)
        for i in range(len(self.generated) - const.N_BACKTEST - 1):
            if (
                self.generated[i] == self.generated[i + const.N_BACKTEST]
                and self.answer[i + const.N_BACKTEST] == True
            ):
                correct_answers += 1
            elif self.answer[i + const.N_BACKTEST] == False:
                correct_answers += 1
        self.callback.message.emit(
            self.callback.Level.DEBUG,
            f"Results calculated: {correct_answers} correct out of {len(self.generated) - const.N_BACKTEST} total questions.",
        )
        self.generated, self.answer = None
        return (correct_answers, len(self.generated) - const.N_BACKTEST)
