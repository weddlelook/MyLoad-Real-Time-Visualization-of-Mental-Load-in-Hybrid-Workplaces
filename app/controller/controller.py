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

        # EEG Listener
        folder_path = os.path.join(os.path.dirname(__file__), '../h5_session_files')
        self.eeg_monitor = EEGMonitoring(create_h5_file(folder_path))
        self.monitorThread = QThread()
        self.eeg_monitor.moveToThread(self.monitorThread)
        self.monitorThread.started.connect(self.eeg_monitor.set_up)

        # GUI
        self.gui = RootWindow()
        self.gui.show()

        # Settings
        self.gui.main_window.settings.back_button.clicked.connect(self.gui.main_window.close_settings)
        self.settings_model = settings.SettingsModel()
        self.gui.main_window.settings.settings_changed.connect(self.settings_model.set)

    def landing_page(self):
        widget = self.gui.main_window.set_page('start')

        # Connect the start button to the monitoring phase
        widget.monitor_start_button.clicked.connect(self.baseline_page)
        widget.monitor_start_button.clicked.connect(self.monitorThread.start)

        widget.settings_button.clicked.connect(self.gui.main_window.open_settings)

        self.monitorThread.started.connect(self.eeg_monitor.record_asr_baseline)

    def baseline_page(self):
        self.gui.main_window.set_page('baseline')

        self.eeg_monitor.baseline_complete_signal.connect(self.eeg_monitor.start_monitoring)
        self.eeg_monitor.baseline_complete_signal.connect(self.monitoring_page)


    def skip_page(self):
        pass

    def monitoring_page(self): 
        widget = self.gui.main_window.set_page('plot')

        # Connect the EEGMonitoring thread to the EEGPlotWidget
        self.eeg_monitor.powers.connect(widget.update_plot)

    def retrospective_page(self):
        pass


    def maxtest_page(self):
        self.gui.main_window.set_page('maxtest')



def create_h5_file(folder_path):
    # TODO: Nutzer ermöglichen, eigenen Session- Namen zu bestimmen.

    # Ordner erstellen, falls er nicht existiert
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    HDF5_FILENAME = os.path.join(folder_path, f"session_{timestamp}.h5")

    # Datei erstellen, falls sie nicht existiert
    if not os.path.exists(HDF5_FILENAME):
        with h5py.File(HDF5_FILENAME, 'w') as h5_file:
            eeg_dtype = np.dtype([('timestamp', 'f8'), ('theta', 'f8'), ('alpha', 'f8'), ('beta', 'f8'),
                                  ('cognitive_load', 'f8')])
            h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
            print(f"HDF5 file created successfully: {HDF5_FILENAME}")
    return HDF5_FILENAME


