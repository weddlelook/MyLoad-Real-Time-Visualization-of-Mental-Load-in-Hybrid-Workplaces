import argparse # argparse is a module that allows you to parse arguments passed to your script when running it from the command line
import asyncio
import numpy as np
import time
import h5py
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
from meegkit.asr import ASR
from brainflow.exit_codes import BrainFlowError
from PyQt6.QtCore import  pyqtSignal, QTimer, QThread, pyqtSlot, QObject

class EEGMonitoring(QObject):
    """
    NOTE: (Regarding pyqtSignals) pyqtSignals are per se just quiet updates, and do not cause any action. They are a way to communicate between threads
    in a thread-safe way. Actual action can be triggered by the connecting a slot.
    """
    powers = pyqtSignal(dict) # contains timestamp, theta, alpha, beta powers, cognitive load that were last calculated
    status_callback = pyqtSignal(str) # Signals current status of the EEG monitor

    #Phase signal
    baseline_complete_signal = pyqtSignal() # Signal that the baseline recording is complete
    min_complete = pyqtSignal()

    NUM_CHANNELS = 8

    def __init__(self, hdf5_file):
        super().__init__()
        self.board_shim = None
        self.sampling_rate = None
        self.asr = None
        self.session_active = False
        self.filename = hdf5_file
        self.monitor_timer = None
        self.phase_timer = None
        self.minwert = 2200
        self.maxwert = 0

        # Buffer for EEG data
        self.data_buffer = None
        self.update_count = 0

        # NOTE: This will be taken out later, but for now lets log all status updates
        self.status_callback.connect(print)

        # NOTE: Starting streaming only once now

    def set_up(self):
        """
        This function sets the timers for both the baseline and the monitoring phase.
        It is mandatory to call this before any of the other functions are called.
        It needs to be called on the thread the EEGMonitoring-Object is supposed to work on.
        Meaning Instantiate > Move to thread > call set_up. This is because of the timers,
        they always belong to the thread they were instatniated on and can only be started and stopped
        in that thread.
        """
        self._connect_board()
        self.board_shim.start_stream()

        # Setting up timer for monitoring function
        self.monitor_timer = QTimer()
        self.monitor_timer.setInterval(1000)  # Update every second
        self.monitor_timer.timeout.connect(self._monitor_cognitive_load)

        # Setting up timer for the phases of recording
        self.phase_timer = QTimer()

    # ------------------------ Phases ----------------------------------------------------

    def record_asr_baseline(self):
        """
        This method starts the Board-Stream and timer for the Baseline recording.
        The private method finish_baseline_recording will be called at the end of the timer to
        process the data internally, once it is done a finish signal will be emitted.
        You can place a slot on that to adjust the GUI/Other appropriatly.
        (signal.connect(slot) <- in case confusion exist about what terminology)
        """
        self.status_callback.emit("Starting ASR Baseline recording for 60 seconds!")
        try:
            self.status_callback.emit("Recording baseline...")
            self.phase_timer = QTimer()
            self.phase_timer.singleShot(3000, self._finish_baseline_recording)

        except BrainFlowError as e:
            self.status_callback(f"BrainFlowError occurred: {e}")

    def record_min(self, time:int):
        """
        Records the minimum cognitive load over the given duration tracks the lowest value
        Value can be accessed via {self.minwert}
        Emits min_complete signal when done

        :time time to record for in milliseconds
        """
        if not self.session_active:
            self.start_monitoring()

        self.status_callback.emit("Starting minimum CL recording")
        if not self.session_active:
            self.start_monitoring()

        def _calculate_min(powers):
            if powers["cognitive_load"] < self.minwert:
                self.minwert = powers["cognitive_load"]
            print("calculate min")

        def _finish_min_recording():
            self.status_callback.emit("finished min recording")
            self.min_complete.emit()
            self.powers.disconnect(_calculate_min)
            print(self.minwert)

        self.powers.connect(_calculate_min)
        self.phase_timer = QTimer()
        self.phase_timer.singleShot(time, _finish_min_recording)

    def record_max(self):
        self.status_callback.emit("Starting maximum CL recording")
        if not self.session_active:
            self.start_monitoring()

        def _calculate_max(powers):
            if powers["cognitive_load"] > self.maxwert:
                self.maxwert = powers["cognitive_load"]
            print("calculate max")

        def _finish_max_recording():
            self.status_callback.emit("finished max recording")
            self.powers.disconnect(_calculate_max)
            self.max_complete.emit()
            print(self.maxwert)

        self.powers.connect(_calculate_max)
        self.phase_timer.singleShot(time, _finish_max_recording)

    # ------------------------ Basic monitoring functionality ---------------------------------

    def start_monitoring(self):
        """
        This method starts the Interval-Timer that ticks every second and connects to the 
        slot function moniter_cognitive_load. This will cause the powers-Signal to be 
        emitted with fresh data every second until the process is paused or shut down.   
        It also will write the data to h5-File specified on __init__
        """
        self.status_callback.emit("Starting EEG recording for video meetings!")
        self.session_active = True

        try:
            self.status_callback.emit("Starting live recording!")

            # Set up the data buffer
            buffer_length = 10 * self.sampling_rate
            self.data_buffer = np.zeros((self.NUM_CHANNELS, buffer_length))

            # Start the streaming session
            self.session_active = True
            self.monitor_timer.start()  # Start the periodic updates using QTimer

        except Exception as e:
            self.status_callback.emit(f"Error during start: {e}")

    def pause_monitoring(self):
        """
        Temporarily stops the monitoring process, no powers will be emitted or files be written
        Resume with resume_monitoring
        """
        try:
            self.session_active = False
            self.monitor_timer.stop()
            self.status_callback.emit("Monitoring stopped")
        except BrainFlowError as e:
            self.status_callback.emit(f"Error stopping monitoring: {e}")

    def resume_monitoring(self):
        """
        Resumes monitoring
        """
        try:
            self.session_active = True
            self.monitor_timer.start()
            self.status_callback.emit("Monitoring resumed")
        except BrainFlowError as e:
            self.status_callback.emit(f"Error resuming monitoring: {e}")

    #----------------- Private methods --------------------

    def _finish_baseline_recording(self):
        print ("Baseline recording finished")
        try:
            # Stop streaming session and get data
            baseline_data = self.board_shim.get_board_data()

            # Preprocess and train ASR, buffer size is 10
            baseline_data = baseline_data[1:9]
            baseline_data_pp = self._preprocess_data(baseline_data, self.sampling_rate)
            #self._train_asr_filter(baseline_data_pp, self.sampling_rate)

            # Emit signal that baseline recording is complete
            self.baseline_complete_signal.emit()

        except BrainFlowError as e:
            self.status_callback.emit(f"BrainFlowError occurred: {e}")

    def _monitor_cognitive_load(self):

        print("Test")

        # Fail-safe, probably not needed
        if not self.session_active:
            self.monitor_timer.stop()
            return

        try:
            new_data = self.board_shim.get_board_data()

            if new_data.shape[0] < self.NUM_CHANNELS:
                raise ValueError(
                    f"Board does not provide enough channels: "
                    f"required {self.NUM_CHANNELS}, got {new_data.shape[0]}")

            if self.update_count > 0:  # Beginne erst nach dem ersten Update mit der Datenerfassung

                transformed_data = new_data[:self.NUM_CHANNELS, :]
                self.data_buffer = np.hstack((self.data_buffer[:, new_data.shape[1]:], transformed_data))

                theta_power, alpha_power, beta_power = self._calculate_powers(self.data_buffer, self.sampling_rate)

                # Data to be emitted
                timestamp = time.time()
                cognitive_load = 0
                if alpha_power != 0:
                    cognitive_load = theta_power / alpha_power
                data = {
                    'timestamp': timestamp,
                    'theta_power': theta_power,
                    'alpha_power': alpha_power,
                    'beta_power': beta_power,
                    'cognitive_load': cognitive_load
                }
                self.powers.emit(data)



                # Speichere die berechneten Werte und den Zeitstempel direkt in die HDF5-Datei
                self._save_eeg_data_as_hdf5(timestamp, theta_power, alpha_power, beta_power, cognitive_load)

            self.update_count += 1

        except Exception as e:
            self.status_callback.emit(f"Error during monitoring: {e}")

    def _save_eeg_data_as_hdf5(self, timestamp, theta_power, alpha_power, beta_power, cognitive_load):
        """
        Speichert die EEG-Daten als HDF5-Datei.
        TODO: Depending on where we implement the calculation of CL out of the powers, we might want to move this function to the controller or implement the calculation of CL here
              The file layout also needs adjustment for the CL if we also store that in the file
        """
        # Neue Daten hinzufügen
        with h5py.File(self.filename, 'a') as h5_file:
            eeg_dataset = h5_file['EEG_data']
            new_index = eeg_dataset.shape[0]

            eeg_dataset.resize((new_index + 1,))
            eeg_dataset[new_index] = (timestamp, theta_power, alpha_power, beta_power, cognitive_load)

    def _preprocess_data(self, data, sfreq):
        for channel in data:
            DataFilter.perform_bandstop(channel, sfreq, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
            DataFilter.perform_bandpass(channel, sfreq, 3.0, 45.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
        return data

    def _train_asr_filter(self, baseline_data, sfreq=250):
        self.asr = ASR(
            sfreq=sfreq,
            cutoff=5,
            blocksize=10,
            win_len=1,
            win_overlap=0.66,
            max_dropout_fraction=0.1,
            min_clean_fraction=0.25,
            method='euclid')
        self.asr.fit(baseline_data)

    def _apply_asr_filter(self, data):
        filtered_data = self.asr.transform(data)
        return filtered_data

    def _calculate_powers(self, data_buffer, sampling_rate):
        theta_powers_per_channel = []
        alpha_powers_per_channel = []
        beta_powers_per_channel = []
        filtered_data_buffer = self._preprocess_data(data_buffer.copy(), sampling_rate)

        for eeg_channel in range(self.NUM_CHANNELS):
            nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
            psd = DataFilter.get_psd_welch(filtered_data_buffer[eeg_channel], nfft, nfft // 2,
                                           sampling_rate, WindowOperations.BLACKMAN_HARRIS.value)

            theta_start = 4
            theta_end = 8
            alpha_start = 8
            alpha_end = 13
            beta_start = 13
            beta_end = 30

            band_power_theta = DataFilter.get_band_power(psd, theta_start, theta_end)
            band_power_alpha = DataFilter.get_band_power(psd, alpha_start, alpha_end)
            band_power_beta = DataFilter.get_band_power(psd, beta_start, beta_end)

            theta_powers_per_channel.append(band_power_theta)
            alpha_powers_per_channel.append(band_power_alpha)
            beta_powers_per_channel.append(band_power_beta)

        return np.mean(np.array(theta_powers_per_channel)), np.mean(np.array(alpha_powers_per_channel)), np.mean(np.array(beta_powers_per_channel))

    def _connect_board(self):
        BoardShim.enable_dev_board_logger()
        parser = argparse.ArgumentParser()

        # Adding arguments to a parser. This makes it possible to pass arguments to the script when starting it.
        # TODO: Since this is not the main entry point, there is little point in doing this here. If somebody wants to clean up that would be lovely
        parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
        parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards', required=False, default=BoardIds.SYNTHETIC_BOARD)
        args = parser.parse_args(['--serial-port', 'COM3', '--board-id', '-1' ]) #BoardIds.CYTON_BOARD

        # Connect to the board
        params = BrainFlowInputParams()
        params.serial_port = args.serial_port
        self.board_shim = BoardShim(args.board_id, params)
        self.board_shim.prepare_session()

        # Set the sampling rate after the board is connected
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_shim.board_id)

        self.status_callback.emit("Connected board")