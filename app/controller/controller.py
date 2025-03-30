from app.controller.pagewrapper import *
import app.model as model
from app.view.rootWindow import RootWindow
from PyQt6.QtCore import pyqtSignal, QObject
import os
import app.model as model

import app.view.pages as widget
from app.util import Logger, getAbsPath, HDF5_FOLDER_PATH


class Controller(QObject):

    start_recording_phase = pyqtSignal(
        int, int
    )  # Signal for threadsafe communication with the recorder, to change recording phase (max/min/paused/monitoring)

    def __init__(self):
        super().__init__()
        self.logger = Logger(
            Logger.Level.INFO
        )
        print(type(self.logger))

        # Model
        self.settings_model = model.SettingsModel(self.logger)
        self.test_model = model.NBackTest(self.logger)
        self.recorder = model.Recorder(self.logger)

        # View
        self.gui = RootWindow(self.settings_model.settings)
        self.gui.retrospective_action.triggered.connect(
            self.gui.main_window.toggle_retrospective
        )

        self.connect_settings()
        self.connect_recorder()

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
        for page_name in self.pages.keys():
            if self.pages[page_name] is not None:
                self.gui.main_window.register_page(
                    self.pages[page_name].widget, page_name
                )

        self.check_last_session()

    def new_session(self):
        self.next_page("start")
        for page_name in self.pages.keys():
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
        self.session_name = session_name
        self.jitsi_room_name = jitsi_room_name
        self.recorder.new_session(self.session_name)

    def next_page(self, page_name: str, *args):
        if not isinstance(page_name, str):
            print(
                f"[ERROR] Invalid page_name: {page_name}. Expected a string."
            )  # Debug-Ausgabe
            return
        try:
            page = self.pages[page_name]
            self.gui.show_toolbar(page.toolbar_shown)
            self.gui.main_window.set_page(page_name)
            page.start(self, *args)
        except KeyError:
            raise  # Wirft den Fehler erneut, um das Programm zu stoppen

    def handle_error(self, e):
        print(f"Error during page change: {e}")

    def connect_settings(self):
        # TODO: Could someone look at this? Is this really the most elegant way to connect the settings?
        self.gui.settings_action.triggered.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.set_settings(self.settings_model.settings)
        self.gui.main_window.settings.new_settings.connect(self.settings_model.set)
        self.gui.main_window.settings.new_settings.connect(self.gui.apply_stylesheet)
        self.gui.main_window.settings.new_settings.connect(
            self.gui.main_window.toggle_settings
        )
        self.gui.main_window.settings.back_button.clicked.connect(
            self.gui.main_window.toggle_settings
        )
        self.gui.main_window.settings.clear_all_button.clicked.connect(
            self.settings_model.clear_sessions
        )

    def connect_recorder(self):
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
        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )  # Ordner, in dem die Datei liegt
        h5_directory = getAbsPath(HDF5_FOLDER_PATH)

        # Falls der Ordner nicht existiert, erstelle ihn
        if not os.path.exists(h5_directory):
            return

        # h5_directory = "app/h5_session_files"
        files = [f for f in os.listdir(h5_directory) if f.endswith(".h5")]
        num_files = len(files)
        matching_files = [f for f in files if f.startswith(f"{num_files}_")]
        if matching_files:
            last_file = matching_files[0]
            model.score.hdf5Util.hdf5File.check_empty_session(h5_directory, h5_directory / last_file, last_file)
