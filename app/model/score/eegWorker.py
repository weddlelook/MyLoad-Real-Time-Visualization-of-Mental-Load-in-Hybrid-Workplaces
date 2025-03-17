import numpy as np
import time
from collections import deque

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
from meegkit.asr import ASR
from brainflow.exit_codes import BrainFlowError

from PyQt6.QtCore import QThread, QObject, pyqtSignal

from .ICAWorker import ICAWorker


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

        # NOTE: Threshold filter
        self.filter_window = deque(maxlen=self.WINDOW_SIZE)

        # NOTE: ICA filter
        self.ica_thread = None
        self.ica_worker = None
        self.ica_model = None

        self.board_id = -1
        self.serial_port = "COM3"

        self.board_shim = None
        self.sampling_rate = None
        self.asr = None
        self.data_buffer = None
        self.update_count = 0  # Ensuring it's initialized

        self.status_callback.connect(print)
        self._start_session()

    def monitor_cognitive_load(self):
        if not self.session_active:
            self._start_session()

        try:
            new_data = self.board_shim.get_board_data()

            if new_data.shape[0] < self.NUM_CHANNELS:
                raise ValueError(
                    f"Board does not provide enough channels: "
                    f"required {self.NUM_CHANNELS}, got {new_data.shape[0]}")

            if self.update_count > 0:
                transformed_data = new_data[:self.NUM_CHANNELS, :]

                self.data_buffer = np.hstack(
                    (self.data_buffer[:, new_data.shape[1]:], transformed_data))

                theta_power, alpha_power, beta_power = self._calculate_powers(
                    self.data_buffer, self.sampling_rate)

                # Data to be emitted
                timestamp = time.time()
                cognitive_load = theta_power / alpha_power if alpha_power != 0 else 0
                data = {
                    'timestamp': timestamp,
                    'theta_power': theta_power,
                    'alpha_power': alpha_power,
                    'beta_power': beta_power,
                    'cognitive_load': cognitive_load
                }
                return data
            else:
                self.update_count += 1
                return None

        except Exception as e:
            self.status_callback.emit(f"Error during monitoring: {e}")

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

    def _preprocess_data(self, data, sfreq):
        for channel in data:
            DataFilter.perform_bandstop(channel, sfreq, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
            DataFilter.perform_bandpass(channel, sfreq, 3.0, 45.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
        return data

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


    def apply_ica(self, new_data):
        """Apply trained ICA to new 1-second EEG chunk."""
        if self.ica_model is None:
            return new_data  # Return raw EEG if ICA isn’t trained yet

        new_data = self.clean_eeg_data(new_data)

        try:
            # Apply ICA transformation
            transformed = np.dot(self.ica_model.components_, new_data)  # Unmix sources
            cleaned_data = np.dot(np.linalg.pinv(self.ica_model.components_), transformed)  # Reconstruct EEG
            return cleaned_data

        except Exception as e:
            self.status_callback.emit(f"Error in ICA application: {e}")
            return new_data  # Return raw data if ICA fails

    def start_ica_training(self):
        """Start ICA training in a separate thread."""
        print("Starting ICA training thread...")

        # Check if enough data is available for training
        if self.data_buffer is None or self.data_buffer.shape[1] < self.sampling_rate * 10:
            print("Not enough data for ICA training. Need at least 10 seconds of EEG.")
            return

        self.ica_thread = QThread()
        data = self.clean_eeg_data(self.data_buffer)

        if np.var(data, axis=1).min() < 1e-6:
            print("Warning: EEG data has very low variance! ICA may fail.")

        self.ica_worker = ICAWorker(data)  # Pass cleaned EEG data
        self.ica_worker.moveToThread(self.ica_thread)

        # Connect signals
        self.ica_thread.started.connect(self.ica_worker.run)
        self.ica_worker.finished.connect(self.store_trained_ica)
        self.ica_worker.finished.connect(self.ica_thread.quit)  # Stop thread when training is done
        self.ica_worker.finished.connect(self.ica_worker.deleteLater)  # Cleanup
        self.ica_thread.finished.connect(self.ica_thread.deleteLater)  # Cleanup

        self.ica_thread.start()

    def store_trained_ica(self, trained_ica):
        """Store the trained ICA model from the worker thread."""
        self.ica_model = trained_ica
        print("New ICA model stored!")

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
