import enum
from PyQt6.QtCore import pyqtSignal, QObject


class Callback(QObject):

    class Level(enum.Enum):
        INFO = 2
        DEBUG = 1
        ERROR = 4

    message = pyqtSignal(Level, str)

    def __init__(self, level: Level = Level.INFO):
        super().__init__()
        self.level = level
        self.message.connect(self._message)

    def _message(self, level: Level, message: str):
        if level.value >= self.level.value:
            print(f"{level.name}: {message}")
