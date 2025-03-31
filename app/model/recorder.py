from app.model.score.eegWorker import EegWorker
from app.model.score.hdf5Util import hdf5File
from app.model.score.calculateScore import ScoreCalculator

from app.util import Logger

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QThread, QObject, QObject, QTimer


import enum


class Phase(enum.Enum):
    MIN = enum.auto()
    MAX = enum.auto()
    PAUSED = enum.auto()
    MONITOR = enum.auto()


class Recorder(QObject):

    powers = pyqtSignal(dict)
    phase_complete = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, logger):
        super().__init__()
        self.logger = logger

        self.hdf5_session = None
        self.score_calculator = None

        self.eegWorker = None
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._start)
        self.thread.start()

        self.minimum = None
        self.maximum = None
        self.phase_flag = Phase.PAUSED.value

    def new_session(self, session_name):
        """Reset the recorder for a new recording session"""
        self.hdf5_session = hdf5File(session_name, self.logger)
        self.minimum = None
        self.maximum = None
        self.phase_flag = Phase.PAUSED.value

    def save_comment(self, timestamp, comment: str):
        """Save a comment to the hdf5-File"""
        self.hdf5_session.save_marker(timestamp, comment)

    def set_phase(self, phase: int, duration: int = None):
        """Change the active phase to the Phase provided"""
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
            if phase == Phase.MIN.value:
                self.logger.message.emit(Logger.Level.INFO, "Minimum phase completed.")
                if not self.minimum:
                    self.error.emit(
                        "No value set yet. Check if your Headphones are set up correctly."
                    )
            if phase == Phase.MAX.value:
                self.logger.message.emit(Logger.Level.INFO, "Maximum phase completed.")
                if not self.maximum:
                    self.error.emit(
                        "No value set yet. Check if your Headphones are set up correctly."
                    )
            if self.minimum and self.maximum:
                self.score_calculator = ScoreCalculator(
                    self.minimum, self.maximum, self.logger
                )
                self.logger.message.emit(
                    Logger.Level.DEBUG,
                    f"Created score calculator with minimum {self.minimum} and maximum {self.maximum}",
                )
            self.phase_complete.emit(phase)

    def _monitor(self):
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
                self.logger.message.emit(
                    Logger.Level.ERROR, "Invalid phase value provided."
                )

    def _start(self):
        """Called when the tread is started"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self._monitor)
        self.monitor_timer.start(1000)
        self.eegWorker = EegWorker(self.logger, self.error)

    def _max_phase(self, data):
        try:
            if not self.maximum or data["raw_cognitive_load"] > self.maximum:
                self.maximum = data["raw_cognitive_load"]
                self.hdf5_session.set_max(self.maximum)
        except TypeError as e:
            self.logger.message.emit(
                Logger.Level.DEBUG,
                "None value recorded.",
            )

    def _min_phase(self, data):
        try:
            if not self.minimum or data["raw_cognitive_load"] < self.minimum:
                self.minimum = data["raw_cognitive_load"]
                self.hdf5_session.set_min(self.minimum)
        except TypeError as e:
            self.logger.message.emit(
                Logger.Level.DEBUG,
                "None value recorded.",
            )

    def _monitoring_phase(self, data):
        try:
            data["load_score"] = self.score_calculator.calculate_score(
                data["cognitive_load"]
            )
            self.logger.message.emit(
                Logger.Level.DEBUG, f"Calculated score: {data["load_score"]}"
            )
            self.hdf5_session.save_eeg_data_as_hdf5(data)
            self.powers.emit(data)
        except TypeError as e:
            self.error.emit(str(e))

    def skip_min_max_phases(self, file_name: str):
        """Omits the minimum and maximum phases by referencing the values from a exitsting file
        :param file_name: the name of the hdf5-file to reference"""
        file = hdf5File.get_h5_file(file_name)
        self.minimum = hdf5File.get_min_value(file)
        self.maximum = hdf5File.get_max_value(file)
        self.hdf5_session.set_min(self.minimum)
        self.hdf5_session.set_max(self.maximum)
        self.score_calculator = ScoreCalculator(self.minimum, self.maximum, self.logger)

    def check_empty_session(self):
        """Check the current hdf5File for missing min and max values"""
        if self.hdf5_session:
            return self.hdf5_session.check_empty_min_max()
        else:
            self.logger.message.emit(Logger.Level.DEBUG, "Cannot check empty session when no hdf5-Session has been initialized")

