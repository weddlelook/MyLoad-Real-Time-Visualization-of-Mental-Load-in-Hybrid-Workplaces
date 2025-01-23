import os
import h5py
import numpy as np
import sys

# Worker thread imports
from PyQt6.QtCore import QThread
from app.model.eegMonitoring import EEGMonitoring

# GUI imports
from PyQt6.QtWidgets import QApplication
from app.view.rootWindow import RootWindow
from app.view.plotWidget import EEGPlotWidget

class Controller(QThread):

    def __init__(self):
        super().__init__()

        # Create an instance of EEGMonitor (which is a worker thread)
        self.eeg_monitor = EEGMonitoring(create_h5_file("test"))

    def setup_gui(self):
        """Setup the GUI and start the application."""
        self.gui = RootWindow()
        self.gui.show()

    def register_slots(self):
        """Connect all the buttons, other signals that are *not specific to 
        a ceratain phase in the lifecycle* here to their respective slots. This could include
        Settings for example."""
        pass

    def monitoring(self):
        """Sets up the monitoring phase of the application."""
 
        # Creating and adding the EEGPlotWidget to the main window
        # TODO: Think about wether this plot _widget should persist or not
        #      If it should persist, then it should be created in the __init__ method
        #      If it shouldn't, cleanup
        plot_widget = EEGPlotWidget()
        self.gui.main_window.add_child(plot_widget)

        # Connect the EEGMonitoring thread to the EEGPlotWidget
        self.eeg_monitor.start()
        self.eeg_monitor.powers.connect(plot_widget.update_plot)

def create_h5_file(filename):
    HDF5_FILENAME = f"{filename}.h5"
    if not os.path.exists(HDF5_FILENAME):
        with h5py.File(HDF5_FILENAME, 'w') as h5_file:
            eeg_dtype = np.dtype([('timestamp', 'f8'), ('theta', 'f8'), ('alpha', 'f8'), ('beta', 'f8')])
            h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
            print("HDF5 file created successfully")
    return HDF5_FILENAME

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.setup_gui()
    controller.monitoring()
    app.exec()
    app.deleteLater()