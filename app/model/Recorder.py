from app.model.score.eegWorker import EegWorker
from app.model.score.hdf5Util import hdf5File
from app.model.score.calculateScore import calculateScore

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QThread, QObject, QObject, QTimer


import enum
import time
import math
import os
from datetime import datetime


class Phase(enum.Enum):
    MIN = enum.auto()
    MAX = enum.auto()
    PAUSED = enum.auto()
    MONITOR = enum.auto()


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
        self.thread.started.connect(self._start)
        self.thread.start()

        self.minimum = None
        self.maximum = None
        self.phase_flag = Phase.PAUSED.value

    def new_session(self, session_name):
        self.hdf5Session = hdf5File(session_name)
        self.minimum = None
        self.maximum = None
        self.phase_flag = Phase.PAUSED.value

    def save_comment(self, timestamp, comment: str):
        self.hdf5Session.save_marker(timestamp, comment)

    def set_phase(self, phase: int, duration: int = None):
        if phase in [e.value for e in Phase]:
            self.phase_flag = phase
            if phase in (Phase.MAX.value, Phase.MIN.value):
                try:
                    QTimer.singleShot(duration, lambda: phase_complete(phase))
                except Exception as e:
                    self.error.emit(f"An error occurred: {str(e)}")
        else:
            # Emit error if phase is not valid
            self.error.emit("Invalid phase value provided.")

        def phase_complete(phase: int):
            self.set_phase(Phase.PAUSED.value, 0)
            if self.minimum and self.maximum:
                print(self.maximum)
                print(self.minimum)
                self.score_calculator = calculateScore(self.minimum, self.maximum)
            self.phase_complete.emit(phase)

    def monitor(self):
        data = self.eegWorker.monitor_cognitive_load()
        match self.phase_flag:
            case Phase.MIN.value:
                self._min_phase(data)
            case Phase.MAX.value:
                self._max_phase(data)
            case Phase.MONITOR.value:
                self._monitoring_phase(data)
            case Phase.PAUSED.value:
                pass
            case _:
                self.error.emit("Invalid phase flag")

    def _start(self):
        """Called when the tread is started"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.monitor)
        self.monitor_timer.start(1000)

    def _max_phase(self, data):
        try:
            if not self.maximum or data["raw_cognitive_load"] > self.maximum:
                self.maximum = data["raw_cognitive_load"]
                self.hdf5Session.set_max(self.maximum)
            print("max")
        except TypeError as e:  # TODO: specify exception
            self.error.emit(str(e))

    def _min_phase(self, data):
        try:
            if not self.minimum or data["raw_cognitive_load"] < self.minimum:
                self.minimum = data["raw_cognitive_load"]
                self.hdf5Session.set_min(self.minimum)
            print("min")
        except TypeError as e:  # TODO: specify exception
            self.error.emit(str(e))

    def _monitoring_phase(self, data):
        try:
            data = self.eegWorker.monitor_cognitive_load()
            data["load_score"] = self.score_calculator.calculatingScore(data)
            self.hdf5Session.save_eeg_data_as_hdf5(data)
            self.powers.emit(data)
            print("monitoring")
        except TypeError as e:
            self.error.emit(str(e))

    def save_previous_min_max_values(self, fileName):
        file = hdf5File.get_h5_file(fileName)
        self.minimum = hdf5File.get_min_value(file)
        self.maximum = hdf5File.get_max_value(file)
        self.hdf5Session.set_min(self.minimum)
        self.hdf5Session.set_max(self.maximum)

        """Could this be solved somehow differnet, eg. in @phase_complete line 61?"""
        self.score_calculator = calculateScore(self.minimum, self.maximum)

    def check_empty_session(self, file_path, fileName):
        file = hdf5File.get_h5_file(fileName)
        minimum = hdf5File.get_min_value(file)
        maximum = hdf5File.get_max_value(file)
        if math.isnan(minimum) or math.isnan(maximum):
            if os.path.exists(file_path):
                os.remove(os.path.join(file_path, fileName))
