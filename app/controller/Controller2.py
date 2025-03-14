from app.controller.PageDTO import *
from app.model import *
from app.model.Recorder import Phase
from app.view.rootWindow import RootWindow
from app.model.score.calculateScore import calculateScore
from PyQt6.QtCore import pyqtSignal, QObject
from app.model.score.hdf5Util import hdf5File


import app.view.pages as widget

class Controller(QObject):

    def __init__(self):
        super().__init__()
        self.recorder = Recorder()
        self.recorder.phase_complete.connect(self.next_page) # TODO
        self.recorder.error.connect(self.handle_error)


        self.settings_model = SettingsModel()
        self.TestLogic = testLogic()
        self.gui = RootWindow(self.settings_model.settings)
        self.gui.retrospective_action.triggered.connect(self.gui.main_window.toggle_retrospective)

        self.connect_settings()
        self.connect_recorder()

        self.hdf5_File = None

        self.pages = {
            "start": StartPage(widget.StartWidget(), self, "baseline_start"),
            "baseline_start": BaselineStartPage(widget.StartBaselinePage(), self, "baseline", "skip"),
            "skip": None,
            "baseline": BaselinePage(widget.BaselineWidget(), self, "maxtest_start"),
            "maxtest_start": MaxtestStartPage(widget.StartMaxTestPage(), self, "maxtest"),
            "maxtest": MaxtestPage(widget.MaxtestPage(), self, "result"),
            "result": ResultPage(widget.ResultsPage(), self, "jitsi"),
            "jitsi": JitsiPage(widget.JitsiWidget(), self, "retrospective", self.settings_model.settings),
            "retrospective": RetrospectivePage(widget.RetrospectivePage("app/h5_session_files"), self)
        }
        
        for page_name in self.pages.keys():
            if self.pages[page_name] is not None:
                self.gui.main_window.register_page(self.pages[page_name].widget, page_name)


    def new_session(self):
        self.next_page("start")
        for page_name in self.pages.keys():
            if self.pages[page_name] is not None:
                self.pages[page_name].reset(self)
        self.session_name = None
        self.jitsi_room_name = None


    def start_min(self):
        self.start_min_signal.emit(1000)

    def start_max(self):
        self.start_max_signal.emit(1000)

    def start_monitoring(self):
        self.start_monitoring_signal.emit()

    def stop_monitoring(self):
        self.recorder.stop_monitoring()

    def set_session_variables(self, session_name:str, jitsi_room_name:str):
        self.session_name = session_name
        self.jitsi_room_name = jitsi_room_name
        self.hdf5_File = hdf5File(session_name)
        self.recorder.new_session(self.hdf5_File)

    def provide_char(self):
        return self.TestLogic.provide_char()
    
    def maxtest_correct_button_clicked(self):
        self.TestLogic.correctButtonClicked()

    def maxtest_incorrect_button_clicked(self):
        self.TestLogic.skipButtonClicked()

    def get_maxtest_result(self):
        self.recorder._set_calculateScore()
        return self.TestLogic.calculateResults()

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
        self.gui.main_window.settings.new_settings.connect(self.changer)

    start_min_signal = pyqtSignal(int)
    start_max_signal = pyqtSignal(int)
    start_monitoring_signal = pyqtSignal()

    def connect_recorder(self):
        self.start_min_signal.connect(self.recorder.min_phase)
        self.start_max_signal.connect(self.recorder.max_phase)
        self.start_monitoring_signal.connect(self.recorder.monitoring_phase)
        self.recorder.phase_complete.connect(self.phase_complete)
        self.recorder.powers.connect(self.testprint)

    def testprint(self, data):
        print("test")

    def phase_complete(self, phase):
        if phase == Phase.MIN_PHASE.value:
            self.next_page("maxtest_start")
        elif phase == Phase.MAX_PHASE.value:
            self.next_page("result")

    def changer(self):
        self.pages["jitsi"].change_display()