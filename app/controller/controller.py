from app.model.eegMonitoring import EEGMonitoring
import os
import asyncio
import h5py
import numpy as np
import sys
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from app.view.rootWindow import RootWindow
from app.view.plotWidget import EEGPlotWidget

def status_callback(message):
    print(message)

async def main():

    # Create an instance of EEGMonitoring
    eeg_monitor = EEGMonitoring(status_callback, create_h5_file("test"))

    # Connect to the board
    eeg_monitor.connect_board()

    # Set up the application and GUI
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    gui = RootWindow()
    eeg_plot_widget = EEGPlotWidget()
    gui.main_window.add_child(eeg_plot_widget)
    gui.show()

    # Record the baseline (takes about 60 seconds)
    await eeg_monitor.record_asr_baseline()

    # Start monitoring and updating the plot
    async def update_plot():
        while True:
            if eeg_monitor.powers:
                print("Updating plot")
                power_data = eeg_monitor.powers
                eeg_plot_widget.update_plot(power_data["timestamp"], power_data["theta_power"], power_data["alpha_power"], power_data["beta_power"])
            await asyncio.sleep(1)  # Adjust the sleep time as needed

    async def monitor_tasks():
        await asyncio.gather(
            eeg_monitor.monitor_cognitive_load(None),
            update_plot()
    )

    with loop:  # Run the event loop
        loop.run_until_complete(monitor_tasks())

def create_h5_file(filename):
    # participant_id = self.participant_id_entry.get()
    # if not participant_id:
    #    self.update_status("Participant ID is required to create HDF5 file")
    #    return

    HDF5_FILENAME = f"{filename}.h5"
    if not os.path.exists(HDF5_FILENAME):
        with h5py.File(HDF5_FILENAME, 'w') as h5_file:
            eeg_dtype = np.dtype([('timestamp', 'f8'), ('theta', 'f8'), ('alpha', 'f8'), ('beta', 'f8')])
            # hr_dtype = np.dtype([('timestamp', 'f8'), ('rr_interval', 'f8'), ('heart_rate', 'f8'), ('raw', 'f8')])
            # keypress_dtype = np.dtype([('timestamp', 'f8'), ('key', 'S10')])
            h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
            print("HDF5 file created successfully")
        # self.root.after(0, self.data_status_icon.config, {"text": "✓", "fg": "green"})
    # else:
        # self.update_status("HDF5 file already exists")
        # self.root.after(0, self.data_status_icon.config, {"text": "✓", "fg": "green"})
    return HDF5_FILENAME

if __name__ == "__main__":
    asyncio.run(main())