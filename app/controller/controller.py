import os
import h5py
import numpy as np
import sys
from datetime import datetime

# Worker thread imports
from app.model.eegMonitoring import EEGMonitoring
from app.model import settings
from PyQt6.QtCore import QThread

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

        # GUI
        self.gui = RootWindow()
        self.gui.show()

        # Settings
        self.gui.main_window.settings.back_button.clicked.connect(self.gui.main_window.close_settings)
        self.settings_model = settings.SettingsModel()
        self.gui.main_window.settings.settings_changed.connect(self.settings_model.set)

    def landing_page(self):
        # Get the start widget and its index
        start_widget = self.gui.main_window.set_page('start')

        # Connect the start button to the monitoring phase
        start_widget.session_name_entered.connect(lambda: self.baseline_page(start_widget.session_name))

        start_widget.settings_button.clicked.connect(self.gui.main_window.open_settings)

        start_widget.retrospective_button.clicked.connect(self.retrospective_page)


    def baseline_page(self, fileName):
        folder_path = os.path.join(os.path.dirname(__file__), '../h5_session_files')
        self.eegWorker = EEGMonitoring(create_h5_file(folder_path, fileName))
        self.eegWorker.moveToThread(self.monitorThread)
        self.monitorThread.started.connect(self.eegWorker.set_up)
        self.monitorThread.started.connect(self.eegWorker.record_asr_baseline)

        self.monitorThread.start()

        self.gui.main_window.set_page('baseline')

        self.eegWorker.baseline_complete_signal.connect(self.eegWorker.start_monitoring)

        self.eegWorker.baseline_complete_signal.connect(self.monitoring_page)


    def skip_page(self):
        pass

    def monitoring_page(self): 
        widget = self.gui.main_window.set_page('plot')

        # Connect the EEGMonitoring thread to the EEGPlotWidget
        self.eegWorker.powers.connect(widget.update_plot)

    def retrospective_page(self):
        retrospective = self.gui.main_window.set_page('retrospective')
        retrospective.back_button.clicked.connect(self.landing_page)



    def maxtest_page(self):
        self.gui.main_window.set_page('maxtest')



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



