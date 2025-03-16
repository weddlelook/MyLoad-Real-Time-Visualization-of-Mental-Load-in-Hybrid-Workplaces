from app.model.score.eegWorker import EegWorker
from app.model.score.hdf5Util import hdf5File
from app.model.score.calculateScore import calculateScore

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QThread, QObject


import enum
import time
from datetime import datetime

class Phase(enum.Enum):
    MIN_PHASE = enum.auto()
    MAX_PHASE = enum.auto()

class Recorder(QObject):

    powers = pyqtSignal(dict)
    phase_complete = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.hdf5Session = None
        self.score_calculator = None

        self.eegWorker = EegWorker()
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.start()

        self.minimum = None
        self.maximum = None
        self.monitoring = False

    def new_session(self, session_name):
        self.hdf5Session = hdf5File(session_name)
        self.minimum = None
        self.maximum = None
        self.monitoring = False

    def min_phase(self, time:int):
        try:
            self.minimum = self.eegWorker.record_minimum(time)
            self.hdf5Session.set_min(self.minimum)
            self.phase_complete.emit(Phase.MIN_PHASE.value)
        except Exception as e: # TODO: specify exception
            self.error.emit(str(e))

    def max_phase(self, time:int):
        try:
            self.maximum = self.eegWorker.record_maximum(time)
            self.hdf5Session.set_max(self.maximum)
            self.phase_complete.emit(Phase.MAX_PHASE.value)
        except Exception as e: # TODO: specify exception
            self.error.emit(str(e))

    def monitoring_phase(self):
        self.monitoring = True
        while self.monitoring:
            try:
                data = self.eegWorker.monitor_cognitive_load()
                data["load_score"] = self.score_calculator.calculatingScore(data)
                self.hdf5Session.save_eeg_data_as_hdf5(data)
                self.powers.emit(data)
                QThread.sleep(1)
            except TypeError as e:
                self.error.emit(str(e))
                QThread.sleep(5)

    def stop_monitoring(self):
        self.monitoring = False

    def _set_calculateScore(self):
        I_Base, I_Max = self.minimum, self.maximum
        self.score_calculator = calculateScore(I_Base, I_Max)

    def save_comment(self, timestamp, comment:str):
        self.hdf5Session.save_marker(timestamp, comment)
