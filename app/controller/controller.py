import os
import h5py
import numpy as np
import sys
from datetime import datetime

# Worker thread imports
from app.model.eegMonitoring import EEGMonitoring
from app.model import settings
from PyQt6.QtCore import QThread
from app.model.testLogic import testLogic

# GUI imports
from app.view.rootWindow import RootWindow


class Controller():

    """
    Each Page in the Lifecycle of the Application is represented by a method in the Controller class.
    Connect your Buttons and similar here, in the respective phases
    """

    def __init__(self):
        super().__init__()

        self.monitorWorker = None  # Instantiate only on session start
        self.monitorThread = QThread()

        #Settings Model
        self.settings_model = settings.SettingsModel()
        # GUI
        self.gui = RootWindow(self.settings_model.settings)
        self.testLogic = testLogic()

        # Settings
        self.gui.settings_action.triggered.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.set_settings(self.settings_model.settings)
        self.gui.main_window.settings.new_settings.connect(self.settings_model.set)
        self.gui.main_window.settings.new_settings.connect(self.gui.apply_stylesheet)
        self.gui.main_window.settings.new_settings.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.back_button.clicked.connect(self.gui.main_window.toggle_settings)
        # Retrospective Page
        self.gui.retrospective_action.triggered.connect(self.gui.main_window.toggle_retrospective)

    def landing_page(self):
        # Get the start widget and its index
        self.gui.show_toolbar(True)
        widget = self.gui.main_window.set_page("start")

        widget.session_name_entered.connect(lambda: self.start_baseline(widget.session_name))

    def start_baseline(self, file_name):
        widget = self.gui.main_window.set_page("baselineStartPage")
        self.gui.show_toolbar(True)
        widget.monitor_baseline_button.clicked.connect(lambda: self.baseline_page(file_name))

    def baseline_page(self, file_name):
        folder_path = os.path.join(os.path.dirname(__file__), '../h5_session_files')
        self.eegWorker = EEGMonitoring(create_h5_file(folder_path, file_name))
        self.eegWorker.moveToThread(self.monitorThread)
        self.monitorThread.started.connect(self.eegWorker.set_up)
        self.monitorThread.started.connect(self.eegWorker.record_asr_baseline)

        self.monitorThread.start()
        self.gui.show_toolbar(False)
        self.gui.main_window.set_page('baseline')

        self.eegWorker.baseline_complete_signal.connect(self.eegWorker.start_monitoring)

        self.eegWorker.baseline_complete_signal.connect(self.start_maxtest_page)

    def skip_page(self):
        pass

    def monitoring_page(self):
        self.gui.show_toolbar(False)
        widget = self.gui.main_window.set_page('plot')
        # Connect the EEGMonitoring thread to the EEGPlotWidget
        self.eegWorker.powers.connect(widget.update_plot)

    #Currently this function is never called instead to open this page toggle_retrospective in mainWidget is called
    def retrospective_page(self):
        self.gui.show_toolbar(True)
        retrospective = self.gui.main_window.set_page('retrospective')
        retrospective.back_button.clicked.connect(self.landing_page)

    def start_maxtest_page(self):
        self.gui.show_toolbar(True)

        startMaxtest_widget = self.gui.main_window.set_page('startmaxtest')


        # Connect the start Button for the maxtest
        startMaxtest_widget.startMaxtestButton.clicked.connect(self.maxtest_page)

        #Connect the skip button for the test
        startMaxtest_widget.skipMaxtestButton.clicked.connect(self.skip_page)

    def maxtest_page(self):
        self.gui.show_toolbar(False)
        widget = self.gui.main_window.set_page('maxtest')
        # Connect the two buttons to skip the next symbol
        widget.correct_button.clicked.connect(self.testLogic.correctButtonClicked)
        widget.skip_button.clicked.connect(self.testLogic.skipButtonClicked)

        self.testLogic.charSubmiter.connect(widget.updateChar)
        self.testLogic.test_timer.timeout.connect(self.results_page)
        self.testLogic.startTest()

    def results_page(self):
        self.gui.show_toolbar(True)
        widget = self.gui.main_window.set_page('result')
        result = self.testLogic.calculateResults()
        widget.updateResult(result)
        # Connect the two buttons to skip the next symbol
        widget.next_button.clicked.connect(self.monitoring_page) # muss noch verbunden werden


def create_h5_file(folder_path, users_session_name):
    # Ordner erstellen, falls er nicht existiert
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Variable welche den Sessions noch eine Nummer gibt, damit diese nummeriert bleiben
    count_of_sessions = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]) + 1


    timestamp = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    HDF5_FILENAME = os.path.join(folder_path, f"{count_of_sessions}__{users_session_name}__{timestamp}.h5")

    # Datei erstellen, falls sie nicht existiert
    if not os.path.exists(HDF5_FILENAME):
        with h5py.File(HDF5_FILENAME, 'w') as h5_file:
            eeg_dtype = np.dtype([('timestamp', 'f8'), ('theta', 'f8'), ('alpha', 'f8'), ('beta', 'f8'),
                                  ('cognitive_load', 'f8')])
            h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
            print(f"HDF5 file created successfully: {HDF5_FILENAME}")
    return HDF5_FILENAME


