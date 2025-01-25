import os
import h5py
import numpy as np
import sys
from datetime import datetime

# Worker thread imports
from model.eegMonitoring import EEGMonitoring
from PyQt6.QtCore import QThread

# GUI imports
from view.rootWindow import RootWindow
from view.plotWidget import EEGPlotWidget
from view.startWidget import StartWidget

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
        self.gui = RootWindow()
        self.gui.show()

    def landing_page(self):
        # Get the start widget and its index
        start_widget = self.gui.main_window.pages['start']
        start_widget_index = self.gui.main_window.layout.indexOf(start_widget)

        # Set the current index of the main window layout to the start widget
        self.gui.main_window.layout.setCurrentIndex(start_widget_index)

        # Connect the start button to the monitoring phase
        start_widget.monitor_start_button.clicked.connect(self.baseline_page)
        start_widget.monitor_start_button.clicked.connect(self.monitorThread.start)
        self.monitorThread.started.connect(self.eeg_monitor.record_asr_baseline)

    def baseline_page(self):
        # Get the start widget and its index
        baseline_widget = self.gui.main_window.pages['baseline']
        baseline_widget_index = self.gui.main_window.layout.indexOf(baseline_widget)

        # Set the current index of the main window layout to the start widget
        self.gui.main_window.layout.setCurrentIndex(baseline_widget_index)

        self.eeg_monitor.baseline_complete_signal.connect(self.eeg_monitor.start_monitoring)
        self.eeg_monitor.baseline_complete_signal.connect(self.monitoring_page)


    def skip_page(self):
        pass

    def monitoring_page(self): 
        # Get the plot widget and its index
        plot_widget = self.gui.main_window.pages['plot']
        plot_widget_index = self.gui.main_window.layout.indexOf(plot_widget)

        # Set the current index of the main window layout to the plot widget
        self.gui.main_window.layout.setCurrentIndex(plot_widget_index)

        # Connect the EEGMonitoring thread to the EEGPlotWidget
        self.eeg_monitor.powers.connect(plot_widget.update_plot)

    def retrospective_page(self):
        pass

def create_h5_file(folder_path):
    # Ordner erstellen, falls er nicht existiert
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    HDF5_FILENAME = os.path.join(folder_path, f"session_{timestamp}.h5")

    # Datei erstellen, falls sie nicht existiert
    if not os.path.exists(HDF5_FILENAME):
        with h5py.File(HDF5_FILENAME, 'w') as h5_file:
            eeg_dtype = np.dtype([('timestamp', 'f8'), ('theta', 'f8'), ('alpha', 'f8'), ('beta', 'f8')])
            h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
            print(f"HDF5 file created successfully: {HDF5_FILENAME}")
    return HDF5_FILENAME

    """
    HDF5_FILENAME = f"{filename}.h5"
    if not os.path.exists(HDF5_FILENAME):
        with h5py.File(HDF5_FILENAME, 'w') as h5_file:
            eeg_dtype = np.dtype([('timestamp', 'f8'), ('theta', 'f8'), ('alpha', 'f8'), ('beta', 'f8')])
            h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
            print("HDF5 file created successfully")
    return HDF5_FILENAME */
    """

