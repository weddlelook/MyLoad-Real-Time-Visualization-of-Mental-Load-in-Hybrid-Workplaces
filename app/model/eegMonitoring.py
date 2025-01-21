import argparse
import asyncio
import numpy as np
import time
import h5py
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
from meegkit.asr import ASR
from brainflow.exit_codes import BrainFlowError

class EEGMonitoring:
    NUM_CHANNELS = 8

    def __init__(self, status_callback, hdf5_file):
        self.board_shim = None
        self.sampling_rate = None
        self.asr = None
        self.session_active = True
        self.status_callback = status_callback 
        self.powers = {}
        self.filename = hdf5_file

    def connect_board(self):
        BoardShim.enable_dev_board_logger()
        parser = argparse.ArgumentParser()

        # Adding arguments to a parser. This makes it possible to pass arguments to the script when starting it.
        # TODO: Since this is not the main entry point, there is little point in doing this here. Why?
        parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
        parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards', required=False, default=BoardIds.SYNTHETIC_BOARD)
        args = parser.parse_args(['--serial-port', 'COM3', '--board-id', '-1'])

        # Connect to the board
        params = BrainFlowInputParams()
        params.serial_port = args.serial_port
        self.board_shim = BoardShim(args.board_id, params)
        self.board_shim.prepare_session()

        # Set the sampling rate after the board is connected
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_shim.board_id)
        print(f"Sampling rate: {self.sampling_rate}")

        self.status_callback("Board connected.")

    def release_board(self):
        if self.board_shim is not None:
            if self.board_shim.is_prepared():
                self.board_shim.release_session()
                self.status_callback("Board session released.")

    def preprocess_data(self, data, sfreq):
        for channel in data:
            DataFilter.perform_bandstop(channel, sfreq, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
            DataFilter.perform_bandpass(channel, sfreq, 3.0, 45.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
        return data

    def train_asr_filter(self, baseline_data, sfreq=250):
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

    def apply_asr_filter(self, data):
        filtered_data = self.asr.transform(data)
        return filtered_data

    def calculate_powers(self, data_buffer, sampling_rate):
        theta_powers_per_channel = []
        alpha_powers_per_channel = []
        beta_powers_per_channel = []
        filtered_data_buffer = self.preprocess_data(data_buffer.copy(), sampling_rate)

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

    async def record_asr_baseline(self):
        self.status_callback("Starting ASR Baseline recording for 60 seconds!")
        try:
            # Start streaming session
            self.board_shim.start_stream()  # Startet die EEG-Aufnahme
            await asyncio.sleep(60)  # Asynchrone Wartezeit, um die GUI und den WebSocket-Client nicht zu blockieren

            # Stop streaming session and get data
            baseline_data = self.board_shim.get_board_data()
            self.board_shim.stop_stream()

            # Preprocess and train ASR
            baseline_data = baseline_data[1:9]
            baseline_data_pp = self.preprocess_data(baseline_data, self.sampling_rate)
            self.train_asr_filter(baseline_data_pp, self.sampling_rate)

        except BrainFlowError as e:
            self.status_callback(f"BrainFlowError occurred: {e}")

    async def monitor_cognitive_load(self, client):

        self.status_callback("Starting EEG recording for video meetings!")

        try:
            self.status_callback("Starting live recording!")

            buffer_length = 10 * self.sampling_rate
            data_buffer = np.zeros((self.NUM_CHANNELS, buffer_length))

            update_count = 0  # Variable zur Zählung der Updates

            async def update():
                nonlocal update_count, data_buffer
                self.status_callback("update function called.")
                try:
                    new_data = self.board_shim.get_board_data()

                    if new_data.shape[0] < self.NUM_CHANNELS:
                        raise ValueError(
                            f"Board does not provide enough channels: "
                            f"required {self.NUM_CHANNELS}, got {new_data.shape[0]}")

                    if update_count > 0:  # Beginne erst nach dem ersten Update mit der Datenerfassung
                        transformed_data = self.apply_asr_filter(new_data[:self.NUM_CHANNELS, :])
                        data_buffer = np.hstack((data_buffer[:, new_data.shape[1]:], transformed_data))

                        theta_power, alpha_power, beta_power = self.calculate_powers(data_buffer, self.sampling_rate)

                        print(f"Theta Power: {theta_power:.2f}, Alpha Power: {alpha_power:.2f}, Beta Power: {beta_power:.2f}")
                        timestamp = time.time()
                        self.powers["timestamp"] = timestamp
                        self.powers["theta_power"] = theta_power
                        self.powers["alpha_power"] = alpha_power
                        self.powers["beta_power"] = beta_power

                        # Speichere die berechneten Werte und den Zeitstempel direkt in die HDF5-Datei
                        self.save_eeg_data_as_hdf5(timestamp, theta_power, alpha_power, beta_power)

                    update_count += 1

                except Exception as e:
                    self.status_callback(f"Error during monitoring: {e}")

            self.board_shim.start_stream()

            while self.session_active:
                await update()
                await asyncio.sleep(1)
            self.status_callback("Exited while loop")

        except BrainFlowError as e:
            self.status_callback(f"BrainFlowError occurred: {e}")

        finally:
            try:
                self.board_shim.stop_stream()
            except BrainFlowError as e:
                self.status_callback(f"Error stopping stream: {e}")

    def save_eeg_data_as_hdf5(self, timestamp, theta_power, alpha_power, beta_power):
        """
        Speichert die EEG-Daten als HDF5-Datei.
        """
        # Neue Daten hinzufügen
        with h5py.File(self.filename, 'a') as h5_file:
            eeg_dataset = h5_file['EEG_data']
            new_index = eeg_dataset.shape[0]

            eeg_dataset.resize((new_index + 1,))
            eeg_dataset[new_index] = (timestamp, theta_power, alpha_power, beta_power)

        self.status_callback(f"EEG Data saved to {self.filename}")