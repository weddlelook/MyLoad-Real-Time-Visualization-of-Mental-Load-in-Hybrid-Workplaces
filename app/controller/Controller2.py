from app.controller.PageDTO import *
from app.model import *
from app.model.Recorder import Phase
from app.view.rootWindow import RootWindow
from app.model.score.calculateScore import calculateScore
from PyQt6.QtCore import pyqtSignal, QObject
from app.model.score.hdf5Util import hdf5File
from app.model.constants import *

import app.view.pages as widget

class Controller(QObject):

    def __init__(self):
        super().__init__()

        # Model
        self.settings_model = SettingsModel()
        self.test_model = testLogic()
        self.recorder = Recorder()

        # View
        self.gui = RootWindow(self.settings_model.settings)
        self.gui.retrospective_action.triggered.connect(self.gui.main_window.toggle_retrospective)

        self.connect_settings()
        self.connect_recorder()

        self.pages = {
            "start": StartPage(widget.StartWidget(), self, "baseline_start"),
            "baseline_start": BaselineStartPage(widget.StartBaselinePage(), self, "baseline", "skip"),
            "skip": SkipPage(widget.SkipPageWidget("app/h5_session_files"), self, "jitsi", "baseline_start"),
            "baseline": BaselinePage(widget.BaselineWidget(), self, "maxtest_start"),
            "maxtest_start": MaxtestStartPage(widget.StartMaxTestPage(), self, "maxtest"),
            "maxtest": MaxtestPage(widget.MaxtestPage(), self, "result"),
            "result": ResultPage(widget.ResultsPage(), self, "jitsi"),
            "jitsi": JitsiPage(widget.JitsiWidget(), self, "retrospective"),
            "retrospective": RetrospectivePage(widget.RetrospectivePage("app/h5_session_files"), self)
        }
        for page_name in self.pages.keys():
            if self.pages[page_name] is not None:
                self.gui.main_window.register_page(self.pages[page_name].widget, page_name)

        self.check_last_session()


    def new_session(self):
        self.next_page("start")
        for page_name in self.pages.keys():
            if self.pages[page_name] is not None:
                self.pages[page_name].reset(self)
        self.session_name = None
        self.jitsi_room_name = None

    def start_min(self):
        self.start_recording_phase.emit(Phase.MIN.value, 1000)

    def start_max(self):
        self.start_recording_phase.emit(Phase.MAX.value, 1000)

    def start_monitoring(self):
        self.start_recording_phase.emit(Phase.MONITOR.value, 0)

    def stop_monitoring(self):
        self.start_recording_phase.emit(Phase.PAUSED.value, 0)

    def set_session_variables(self, session_name:str, jitsi_room_name:str):
        self.session_name = session_name
        self.jitsi_room_name = jitsi_room_name  
        self.recorder.new_session(self.session_name)

    def provide_char(self):
        return self.test_model.provide_char()
    
    def maxtest_correct_button_clicked(self):
        self.test_model.correctButtonClicked()

    def maxtest_incorrect_button_clicked(self):
        self.test_model.skipButtonClicked()

    def get_maxtest_result(self):
        return self.test_model.calculateResults()

    def next_page(self, page_name:str, *args):
            #page = self.pages[page_name]
            #print(f"Changing to page {page_name}")
            #self.gui.show_toolbar(page.toolbar_shown)
            #self.gui.main_window.set_page(page_name)
            #page.start(self, *args)
            print(f"[DEBUG] next_page called with page_name: {page_name} (type: {type(page_name)})")  # Debug-Ausgabe
            if not isinstance(page_name, str):
                print(f"[ERROR] Invalid page_name: {page_name}. Expected a string.")  # Debug-Ausgabe
                return
            try:
                page = self.pages[page_name]
                print(f"[DEBUG] Changing to page {page_name}")  # Debug-Ausgabe
                self.gui.show_toolbar(page.toolbar_shown)
                self.gui.main_window.set_page(page_name)
                page.start(self, *args)
            except KeyError:
                print(
                    f"[ERROR] Invalid page_name: {page_name}. Valid keys are: {list(self.pages.keys())}")  # Debug-Ausgabe
                raise  # Wirft den Fehler erneut, um das Programm zu stoppen

    def handle_error(self, e):
        print(f"Error during page change: {e}")

    def connect_settings(self):
        # TODO: Could someone look at this? Is this really the most elegant way to connect the settings?
        self.gui.settings_action.triggered.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.set_settings(self.settings_model.settings)
        self.gui.main_window.settings.new_settings.connect(self.settings_model.set)
        self.gui.main_window.settings.new_settings.connect(self.gui.apply_stylesheet)
        self.gui.main_window.settings.new_settings.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.back_button.clicked.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.clear_all_button.clicked.connect(self.settings_model.clear_sessions)

    start_recording_phase = pyqtSignal(int, int)

    def connect_recorder(self):
        self.start_recording_phase.connect(self.recorder.set_phase)
        self.recorder.phase_complete.connect(self.phase_complete)
        self.recorder.phase_complete.connect(self.next_page) # TODO
        self.recorder.error.connect(self.handle_error)

    def phase_complete(self, phase):
        if phase == Phase.MIN.value:
            self.next_page("maxtest_start")
        elif phase == Phase.MAX.value:
            self.next_page("result")

    def check_last_session(self):
        h5_directory = "app/h5_session_files"
        files = [f for f in os.listdir(h5_directory) if f.endswith(".h5")]
        num_files = len(files)
        matching_files = [f for f in files if f.startswith(f"{num_files}_")]
        if matching_files:
            last_file = matching_files[0]
            self.recorder.check_empty_session(h5_directory, last_file)
