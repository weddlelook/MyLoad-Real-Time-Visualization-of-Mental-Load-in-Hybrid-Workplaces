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
from app.model.calculateScore import calculateScore
from app.model.hdf5Util import hdf5File

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

        # Models
        self.eegWorker = EEGMonitoring()
        self.settings_model = settings.SettingsModel()
        self.testLogic = testLogic()
        self.calculateScore = None # Instantiate after max_complete signal
        self.sessionFile = None

        # View
        self.gui = RootWindow(self.settings_model.settings)

        # Settings
        self.gui.settings_action.triggered.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.set_settings(self.settings_model.settings)
        self.gui.main_window.settings.new_settings.connect(self.settings_model.set)
        self.gui.main_window.settings.new_settings.connect(self.gui.apply_stylesheet)
        self.gui.main_window.settings.new_settings.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.back_button.clicked.connect(self.gui.main_window.toggle_settings)
        self.gui.main_window.settings.clear_all_button.clicked.connect(self.settings_model.clear_sessions)
        # Retrospective Page
        self.gui.retrospective_action.triggered.connect(self.gui.main_window.toggle_retrospective)

    def landing_page(self):
        # Get the start widget and its index
        self.gui.show_toolbar(True)
        widget = self.gui.main_window.set_page("start")
        widget.session_input.clear()
        widget.jitsi_input.clear()

        # saving room name in controller object, so that we reach it later 
        widget.user_input_entered.connect(lambda: self.set_room_name(widget.jitsi_room_name))
        # opening start baseline page 
        widget.user_input_entered.connect(lambda: self.start_baseline(widget.session_name))
        

    def set_room_name(self, room_name): 
        self.jitsi_room_name = room_name
    

    def start_baseline(self, file_name):
        widget = self.gui.main_window.set_page("baselineStartPage")
        self.gui.show_toolbar(True)
        widget.monitor_baseline_button.clicked.connect(lambda: self.baseline_page(file_name))

    def baseline_page(self, file_name):
        self.sessionFile = hdf5File(file_name)
        self.eegWorker.moveToThread(self.monitorThread)
        self.monitorThread.started.connect(self.eegWorker.set_up)
        self.monitorThread.started.connect(lambda: self.eegWorker.record_min(10000))

        self.monitorThread.start()
        self.gui.show_toolbar(False)
        self.gui.main_window.set_page('baseline')

        self.eegWorker.baseline_complete.connect(self.eegWorker.start_monitoring)

        self.eegWorker.min_complete.connect(self.start_maxtest_page)

    def skip_page(self):
        pass


    def start_maxtest_page(self):
        self.gui.show_toolbar(False)

        startMaxtest_widget = self.gui.main_window.set_page('startmaxtest')


        # Connect the start Button for the maxtest
        startMaxtest_widget.startMaxtestButton.clicked.connect(self.maxtest_page)

        #Connect the skip button for the test
        startMaxtest_widget.skipMaxtestButton.clicked.connect(self.jitsi_page)

    def maxtest_page(self):
        self.gui.show_toolbar(False)
        widget = self.gui.main_window.set_page('maxtest')
        # Connect the two buttons to skip the next symbol
        widget.correct_button.clicked.connect(self.testLogic.correctButtonClicked)
        widget.skip_button.clicked.connect(self.testLogic.skipButtonClicked)

        self.eegWorker.record_max(10000)

        self.testLogic.showButton.connect(widget.show_correct_button)

        self.testLogic.charSubmiter.connect(widget.updateChar)
        self.eegWorker.max_complete.connect(self.results_page)
        #self.testLogic.test_timer.timeout.connect(self.results_page)
        self.testLogic.startTest()

        self.eegWorker.max_complete.connect(self._set_calculateScore)

    def _set_calculateScore(self):
            I_Base, I_Max = self.eegWorker.minwert, self.eegWorker.maxwert
            self.calculateScore = calculateScore(I_Base, I_Max)

    def results_page(self):
        self.gui.show_toolbar(False)
        widget = self.gui.main_window.set_page('result')
        result = self.testLogic.calculateResults()
        widget.updateResult(result)
        # Connect the two buttons to skip the next symbol
        # I changed the connection from plotWidget to JitsiWidget for testing the jitsi page
        widget.next_button.clicked.connect(self.jitsi_page) # muss noch verbunden werden

    def jitsi_page(self): 
        self.eegWorker.powers.connect(self.sessionFile.save_eeg_data_as_hdf5)
        self.gui.show_toolbar(True)
        jitsi_widget = self.gui.main_window.set_page("jitsi")
        # takes the room name from controller object and gives it to the jitsi view
        jitsi_widget.load_jitsi_meeting(self.jitsi_room_name)
        jitsi_widget.end_button.clicked.connect(jitsi_widget.end_meeting) # button for ending the meeting
        jitsi_widget.end_button.clicked.connect(self.retrospective_page) # button for ending the meeting


        '''
        I added the plot widget to the jitsi page, so that we can see the plot too. I think this is not the best way
        to do it, but i am leaving it so for now
        '''
        plot_widget = jitsi_widget.plot_widget
        # Connect the EEGMonitoring thread to the EEGPlotWidget
        self.eegWorker.powers.connect(plot_widget.update_plot)
        self.eegWorker.powers.connect(self.calculateScore.calculatingScore)
        self.calculateScore.score.connect(plot_widget.updateScore)

    #Currently this function is never called instead to open this page toggle_retrospective in mainWidget is called
    def retrospective_page(self):
        self.gui.show_toolbar(True)
        widget = self.gui.main_window.set_page('retrospective')
        widget.load_sessions()
        widget.back_button.clicked.connect(self.landing_page)


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


