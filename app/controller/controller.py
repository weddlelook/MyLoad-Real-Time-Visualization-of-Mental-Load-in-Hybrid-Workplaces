import os
import h5py
import numpy as np
import sys
from datetime import datetime


#util
# from app.controller.util import *

# Worker thread imports
from app.model.eegMonitoring import EEGMonitoring

# GUI imports
from PyQt6.QtWidgets import QApplication
from app.view.rootWindow import RootWindow
from app.view.plotWidget import EEGPlotWidget
from app.view.startWidget import StartWidget

class Controller():

    def __init__(self):
        super().__init__()


        folder_path = os.path.join(os.path.dirname(__file__), '../h5_session_files')
        # Create an instance of EEGMonitor (which is a worker thread)
        self.eeg_monitor = EEGMonitoring(create_h5_file(folder_path))

    def setup_gui(self):
        """Setup the GUI and start the application."""
        self.gui = RootWindow()
        self.gui.show()

    def register_slots(self):
        """Connect all the buttons, other signals that are *not specific to 
        a ceratain phase in the lifecycle* here to their respective slots. This could include
        Settings for example."""
        pass

    def landing_page(self):
        """Sets up the landing page of the application."""

        # Get the start widget and its index
        start_widget = self.gui.main_window.pages['start']
        start_widget_index = self.gui.main_window.layout.indexOf(start_widget)

        # Set the current index of the main window layout to the start widget
        self.gui.main_window.layout.setCurrentIndex(start_widget_index)

        # Connect the start button to the monitoring phase
        start_widget.monitor_start_button.clicked.connect(self.monitoring)

    def monitoring(self):
        """Sets up the monitoring phase of the application."""
 
        # Get the plot widget and its index
        plot_widget = self.gui.main_window.pages['plot']
        plot_widget_index = self.gui.main_window.layout.indexOf(plot_widget)

        # Set the current index of the main window layout to the plot widget
        self.gui.main_window.layout.setCurrentIndex(plot_widget_index)

        # Connect the EEGMonitoring thread to the EEGPlotWidget
        self.eeg_monitor.start()
        self.eeg_monitor.powers.connect(plot_widget.update_plot)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.setup_gui()
    controller.landing_page()
    app.exec()
    app.deleteLater()

