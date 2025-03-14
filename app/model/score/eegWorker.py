import numpy as np
import time
from collections import deque

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
from meegkit.asr import ASR
from brainflow.exit_codes import BrainFlowError

from PyQt6.QtCore import  QThread, QObject, pyqtSignal


class EegWorker(QObject):

    status_callback = pyqtSignal(str)

    NUM_CHANNELS = 8
    WINDOW_SIZE = 5
    MIN_WINDOW_SIZE = 3
    THRESHOLD_UPPER = 20
    THRESHOLD_LOWER = 0.1

    def __init__(self):
        super().__init__()
        self.session_active = False
        self.databuffer = None

        self.filter_window= deque(maxlen=self.WINDOW_SIZE)

        self.board_id = -1
        self.serial_port = "COM3"

        self.board_shim = None
        self.sampling_rate = None
        self.asr = None
        self.data_buffer = None
        self.update_count = None

        self.status_callback.connect(print) 
        self._start_session()   

    def monitor_cognitive_load(self):
        if not self.session_active:
            self._start_session()
            QThread.msleep(1000)

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
                    'cognitive_load': self._filter_cl(cognitive_load)
                }
                return data
            else:
                self.update_count += 1
                return None

        except Exception as e:
            self.status_callback.emit(f"Error during monitoring: {e}")

    # ------------------ Phases -----------------------

    def record_minimum(self, time:int):
        if not self.session_active:
            self._start_session()

        self.status_callback.emit("Recording minimum cognitive load")
        minwert = 100
        faults = 0 
        faults = 0 

        while time > 0:
            QThread.msleep(1000)
            data = self.monitor_cognitive_load()
            try: 
                try: 
                if data['cognitive_load'] < minwert:
                        minwert = data['cognitive_load']
            except TypeError:
                faults += 1
            except TypeError:
                faults += 1
            time -= 1000
    
        if minwert == 100:
            raise ValueError("No valid data recorded")
        
        self.status_callback.emit(f"Minimum cognitive load: {minwert} with {faults} faults with {faults} faults")
        return minwert
    
    def record_maximum(self, time:int):
        if not self.session_active:
            self._start_session()

        self.status_callback.emit("Recording maximum cognitive load")
        maxwert = 0
        faults = 0
        faults = 0

        while time > 0:
            QThread.msleep(1000)
            data = self.monitor_cognitive_load()
            try:
                try:
                if data['cognitive_load'] > maxwert:
                        maxwert = data['cognitive_load']
            except TypeError:
                faults += 1
            except TypeError:
                faults += 1
            time -= 1000

        if maxwert == 0:
            raise ValueError("No valid data recorded")
        
        self.status_callback.emit(f"Maximum cognitive load: {maxwert} with {faults} faults with {faults} faults")
        return maxwert    

    # --------------- Private methods -----------------

    def _connect_board(self):
        BoardShim.enable_dev_board_logger()

        # Connect to the board
        params = BrainFlowInputParams()
        params.serial_port = self.serial_port
        self.board_shim = BoardShim(self.board_id, params)
        self.board_shim.prepare_session()

        # Set the sampling rate after the board is connected
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_shim.board_id)

        self.status_callback.emit("Connected board")

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

    def _preprocess_data(self, data, sfreq):
        for channel in data:
            DataFilter.perform_bandstop(channel, sfreq, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
            DataFilter.perform_bandpass(channel, sfreq, 3.0, 45.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
        return data
    
    def _filter_cl(self, cl_value):
        """
        Replace invalid cognitive load values with mean of prior valid values.
        
        :return: Valid value as given, average if invalid or none if the value is invalid and not enough valid values are available in the sliding window.
        """

        # Append value if valid, otherwise append None
        if self.THRESHOLD_LOWER <= cl_value <= self.THRESHOLD_UPPER:
            self.filter_window.append(cl_value) 
            return cl_value
        else:
            self.filter_window.append(None)

        # Filter for valid values
        valid_values = [v for v in self.filter_window if v is not None]

        if len(valid_values) >= self.MIN_WINDOW_SIZE:
            return np.mean(valid_values)
        else:  
            return None

    def _start_session(self):
        self._connect_board()
        self.board_shim.start_stream()
        self.status_callback.emit("Started session")
        self.session_active = True
        buffer_length = 10 * self.sampling_rate
        self.data_buffer = np.zeros((self.NUM_CHANNELS, buffer_length))
        self.update_count = 0
        QThread.msleep(1000)
        self.monitor_cognitive_load()