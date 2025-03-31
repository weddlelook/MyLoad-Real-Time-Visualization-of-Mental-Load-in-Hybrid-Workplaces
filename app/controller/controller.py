from app.controller.pagewrapper import *
import app.model as model
from app.view.rootWindow import RootWindow
from PyQt6.QtCore import pyqtSignal, QObject
import os
import app.model as model

import app.view.pages as widget
from app.util import Logger, getAbsPath, HDF5_FOLDER_PATH, LOGGER_LEVEL


class Controller(QObject):

    start_recording_phase = pyqtSignal(
        int, int
    )  # Signal for threadsafe communication with the recorder, to change recording phase (max/min/paused/monitoring)

    def __init__(self):
        super().__init__()
        self.logger = Logger(LOGGER_LEVEL)

        # Model
        self.settings_model = model.SettingsModel(self.logger)
        self.test_model = model.NBackTest(self.logger)
        self.recorder = model.Recorder(self.logger)

        # View
        self.gui = RootWindow(self.settings_model.settings)

        self._connect_settings() 
        self._connect_recorder()

        self.pages = {
            "start": StartPage(widget.StartWidget(), self, "baseline_start"),
            "baseline_start": BaselineStartPage(
                widget.StartBaselinePage(), self, "baseline", "skip"
            ),
            "skip": SkipPage(
                widget.SkipPageWidget("app/h5_session_files"),
                self,
                "jitsi",
                "baseline_start",
            ),
            "baseline": BaselinePage(widget.BaselineWidget(), self, "maxtest_start"),
            "maxtest_start": MaxtestStartPage(
                widget.StartMaxTestPage(), self, "maxtest"
            ),
            "maxtest": MaxtestPage(widget.MaxtestPage(), self, "result"),
            "result": ResultPage(widget.ResultsPage(), self, "jitsi"),
            "jitsi": JitsiPage(widget.JitsiPage(), self, "retrospective"),
            "retrospective": RetrospectivePage(
                widget.RetrospectivePage("app/h5_session_files"), self
            ),
        }
        for page_name in self.pages.keys(): # Registering the widgets wrapped in the page dict with the view
            if self.pages[page_name] is not None:
                self.gui.main_window.register_page(
                    self.pages[page_name].widget, page_name
                )

        self.session_name = None
        self.jitsi_room_name = None

    def new_session(self):
        """Resetting variables and view for a new session"""
        self.next_page("start")
        for page_name in self.pages.keys(): # Resetting each page in pages
            if self.pages[page_name] is not None:
                self.pages[page_name].reset(self)
        self.session_name = None
        self.jitsi_room_name = None

    def phase_change(self, phase: int, time: int = 0):
        """Emit the phase change signal to the recorder thread.
        :param phase: The value of phase to change to (e.g., MIN, MAX, MONITORING), see Phase class in model.recorder.
        :param time: The time in milliseconds for the phase to last. Only relevant for MIN and MAX phases.
        """
        self.start_recording_phase.emit(phase, time)

    def set_session_variables(self, session_name: str, jitsi_room_name: str):
        """Set the session and jitsi_room_name so a new recorder session can be started"""
        self.session_name = session_name
        self.jitsi_room_name = jitsi_room_name
        self.recorder.new_session(self.session_name)

    def next_page(self, page_name: str, *args):
        """Moving the view to the page specified"""
        page = self.pages[page_name]
        self.gui.show_toolbar(page.toolbar_shown)
        self.gui.main_window.set_page(page_name)
        page.start(self, *args)


    def handle_error(self, error_message: str):
        self.gui.display_error_message(
            error_message,
        )
        self.logger.message.emit(
            Logger.Level.ERROR, f"Error in Recorder: {error_message}"
        )
        if error_message.startswith("No value set yet"):
            self.next_page("baseline_start")
            self.pages["baseline"].reset(self)
            self.pages["maxtest"].reset(self)
            self.phase_change(Phase.PAUSED.value, 0)

    def _connect_settings(self):
        self.gui.main_window.settings.new_settings.connect(self.settings_model.set)
        self.gui.main_window.settings.set_settings(self.settings_model.settings)

    def _connect_recorder(self):
        self.start_recording_phase.connect(self.recorder.set_phase)
        self.recorder.phase_complete.connect(self._phase_complete)
        self.recorder.error.connect(self.handle_error)

    def _phase_complete(self, phase):
        """Slot connected to the recorder's phase_complete signal. Facilitates page changes that are dependent on recorder phases. Rather than view signals."""
        if phase == Phase.MIN.value:
            self.next_page("maxtest_start")
        elif phase == Phase.MAX.value:
            self.next_page("result")

    def check_last_session(self):

        # Nothing to check if the folder does not exist or session isn't started
        if not os.path.exists(getAbsPath(HDF5_FOLDER_PATH)) or not self.session_name:
            self.logger.message.emit(Logger.Level.DEBUG, "Can't check session, no file exists")
            return

        full_path = self.recorder.check_empty_session() # Function will return the full path if min/max are unset

        if full_path:
            self.logger.message.emit(Logger.Level.INFO, f"Deleting file {full_path}")
            os.remove(full_path)

    def deleteLater(self):
        self.logger.message.emit(Logger.Level.DEBUG, "Closing controller")
        self.check_last_session()
        super().deleteLater()