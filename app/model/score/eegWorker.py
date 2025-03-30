import numpy as np
import time
from collections import deque
import argparse

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
from brainflow.exit_codes import BrainFlowError

from PyQt6.QtCore import QThread, QObject, pyqtSignal

from app.util import Logger, WINDOW_SIZE, THRESHOLD_UPPER, NUM_CHANNELS

class EegWorker(QObject):

    def __init__(self, logger: Logger, error: pyqtSignal):
        super().__init__()
        self.session_active = False
        self.sliding_window = None # deque for the moving average

        parser = argparse.ArgumentParser(description="board parameters")
        parser.add_argument(
            "--port",
            type=str,
            help="Name of the bluetooth port the board receiver is connected to",
            default="COM3",
        )
        parser.add_argument(
            "--board_id",
            type=int,
            help="Id of the Board connected, -1 for synthetic",
            default=-1,
        )
        args = parser.parse_args()
        self.board_id = args.board_id
        self.serial_port = args.port

        self.board_shim = None
        self.sampling_rate = None
        self.data_buffer = None
        self.update_count = 0

        self.logger = logger
        self.error = error

        self._start_session()

    # --------------- Set up -----------------

    def _start_session(self):
        self._connect_board()
        self.board_shim.start_stream()
        self.logger.message.emit(Logger.Level.DEBUG, "Started monitoring session")
        self.sliding_window = deque(maxlen=WINDOW_SIZE)

        self.session_active = True
        buffer_length = 10 * self.sampling_rate
        self.data_buffer = np.zeros((NUM_CHANNELS, buffer_length))
        self.update_count = 0
        QThread.msleep(1000)
        self.monitor_cognitive_load()

    def _connect_board(self):
        if self.logger.level == Logger.Level.DEBUG:
            BoardShim.enable_dev_board_logger()

        # Connect to the board
        params = BrainFlowInputParams()
        params.serial_port = self.serial_port
        try:
            self.board_shim = BoardShim(self.board_id, params)
            self.board_shim.prepare_session()
        except BrainFlowError as e:
            self.error.emit(f"An error has occurred while connecting the board: {e}")

        # Set the sampling rate after the board is connected
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_shim.board_id)

        self.logger.message.emit(
            Logger.Level.DEBUG,
            f"Board is connected with USB-port {self.serial_port} and board-id {self.board_id}",
        )

    # -------------- Monitor --------------------

    def monitor_cognitive_load(self) -> dict:
        """Fetches data from the board, calculates the load_index
        :returns: A dictionary containing the keys 
            > timestamp: The unix epoch-second the load was calculated at
            > raw_cognitive_load: The calculated load, processed through a threshhold filter
            > cognitive_load: The moving average over the raw_cognitive_load
            with str values
            IF an error occurs or the board produces unreliable data for an extended amount of time, 
            the value of the last two keys will be None,
            The first update after starting a session will always return None instead of a dict
        """
        if not self.session_active:
            self._start_session()

        try:
            new_data = self.board_shim.get_board_data()

            if new_data.shape[0] < NUM_CHANNELS:
                raise ValueError(
                    f"Board does not provide enough channels: "
                    f"required {NUM_CHANNELS}, got {new_data.shape[0]}"
                )

            if self.update_count > 0:
                transformed_data = new_data[: NUM_CHANNELS, :]

                self.data_buffer = np.hstack(
                    (self.data_buffer[:, new_data.shape[1] :], transformed_data)
                )

                theta_power, alpha_power, beta_power = self._calculate_powers(
                    self.data_buffer, self.sampling_rate
                )

                # Data to be emitted
                timestamp = time.time()
                cognitive_load = theta_power / alpha_power if alpha_power != 0 else 0
                data = {
                    "timestamp": timestamp,
                    "raw_cognitive_load": self._threshold_filter(cognitive_load),
                    "cognitive_load": self._moving_average(),
                }
                self.logger.message.emit(
                    Logger.Level.DEBUG,
                    f"Monitored CL: {data['cognitive_load']}, without moving average {data['raw_cognitive_load']}",
                )
                self.update_count += 1
                return data
            else:
                self.update_count += 1
                return None

        except Exception as e:
            self.error.emit(f"Error during monitoring: {e}")

    def _preprocess_data(self, data, sfreq):
        for channel in data:
            DataFilter.perform_bandstop(
                channel,
                sfreq,
                48.0,
                52.0,
                2,
                FilterTypes.BUTTERWORTH_ZERO_PHASE.value,
                0,
            )
            DataFilter.perform_bandpass(
                channel,
                sfreq,
                3.0,
                45.0,
                2,
                FilterTypes.BUTTERWORTH_ZERO_PHASE.value,
                0,
            )
        return data

    def _calculate_powers(self, data_buffer, sampling_rate):
        theta_powers_per_channel = []
        alpha_powers_per_channel = []
        beta_powers_per_channel = []
        filtered_data_buffer = self._preprocess_data(data_buffer.copy(), sampling_rate)

        for eeg_channel in range(NUM_CHANNELS):
            nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
            psd = DataFilter.get_psd_welch(
                filtered_data_buffer[eeg_channel],
                nfft,
                nfft // 2,
                sampling_rate,
                WindowOperations.BLACKMAN_HARRIS.value,
            )

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

        return (
            np.mean(np.array(theta_powers_per_channel)),
            np.mean(np.array(alpha_powers_per_channel)),
            np.mean(np.array(beta_powers_per_channel)),
        )

    def _threshold_filter(self, cl_value):
        if cl_value <= THRESHOLD_UPPER:
            self.sliding_window.append(cl_value)
            return cl_value
        else:
            self.sliding_window.append(None)
            return None

    def _moving_average(self):
        valid_values = [v for v in self.sliding_window if v is not None]
        return np.mean(valid_values) if valid_values else None
