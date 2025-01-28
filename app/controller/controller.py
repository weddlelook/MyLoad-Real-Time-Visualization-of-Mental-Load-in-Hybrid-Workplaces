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

        folder_path = os.path.join(os.path.dirname(__file__), '../h5_session_files')
        # Create an instance of EEGMonitor (which is a worker thread)
        self.eeg_monitor = EEGMonitoring(create_h5_file(folder_path))
        self.monitorThread = QThread()
        self.eeg_monitor.moveToThread(self.monitorThread)
        self.monitorThread.started.connect(self.eeg_monitor.set_up)
        self.settings_model = settings.SettingsModel()
        self.gui = RootWindow(self.settings_model.settings)
        self.actual_widget_index = None

    def _update_index(self, index):
        self.actual_widget_index = index

    def landing_page(self):
        # Get the start widget and its index
        widget = self.gui.main_window.pages['start']
        widget_index = self.gui.main_window.layout.indexOf(widget)

        # Set the current index of the main window layout to the start widget
        self.gui.main_window.layout.setCurrentIndex(widget_index)
        self._update_index(widget_index)

        # Connect the start button to the monitoring phase
        widget.start_session_button.clicked.connect(self.start_baseline)
        widget.settings_button.clicked.connect(self.open_settings)

    def start_baseline(self):
        widget = self.gui.main_window.pages["baselineStartPage"]
        widget_index = self.gui.main_window.layout.indexOf(widget)

        self.gui.main_window.layout.setCurrentIndex(widget_index)
        self._update_index(widget_index)

        widget.monitor_baseline_button.clicked.connect(self.baseline_page)
        widget.monitor_baseline_button.clicked.connect(self.monitorThread.start)
        self.monitorThread.started.connect(self.eeg_monitor.record_asr_baseline)

    def baseline_page(self):
        # Get the start widget and its index
        widget = self.gui.main_window.pages['baseline']
        widget_index = self.gui.main_window.layout.indexOf(widget)

        # Set the current index of the main window layout to the start widget
        self.gui.main_window.layout.setCurrentIndex(widget_index)

        self.eeg_monitor.baseline_complete_signal.connect(self.eeg_monitor.start_monitoring)
        self.eeg_monitor.baseline_complete_signal.connect(self.monitoring_page)


    def skip_page(self):
        pass

    def monitoring_page(self): 
        # Get the plot widget and its index
        widget = self.gui.main_window.pages['plot']
        widget_index = self.gui.main_window.layout.indexOf(widget)

        # Set the current index of the main window layout to the plot widget
        self.gui.main_window.layout.setCurrentIndex(widget_index)
        self._update_index(widget_index)


        # Connect the EEGMonitoring thread to the EEGPlotWidget
        self.eeg_monitor.powers.connect(widget.update_plot)

    def retrospective_page(self):
        pass


    def maxtest_page(self):
        # Get the start widget and its index
        widget = self.gui.main_window.pages['maxtest']
        widget_index = self.gui.main_window.layout.indexOf(widget)

        # Set the current index of the main window layout to the start widget
        self.gui.main_window.layout.setCurrentIndex(widget_index)
        self._update_index(widget_index)

        # Connect the two buttons to skip the next symbol

    def open_settings(self):
        widget = self.gui.main_window.pages['settings']
        widget.set_settings(self.settings_model.settings)
        widget_index = self.gui.main_window.layout.indexOf(widget)

        self.gui.main_window.layout.setCurrentIndex(widget_index)

        widget.new_settings.connect(self.settings_model.set)
        widget.settings_changed.connect(self.gui.apply_stylesheet)
        widget.settings_changed.connect(self.go_back_to_previous_page)
        widget.back_button.clicked.connect(self.go_back_to_previous_page)

    def go_back_to_previous_page(self):
        self.gui.main_window.layout.setCurrentIndex(self.actual_widget_index)


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


