import queue
import asyncio
from asyncio import Queue
import time
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
from brainflow.exit_codes import BrainFlowError
from meegkit.asr import ASR
import argparse
import tkinter as tk
from tkinter import ttk
import json
import os
import h5py
from bleak import BleakScanner, BleakClient
import keyboard

HDF5_FILENAME = None

class EEGMonitoring:
    NUM_CHANNELS = 8

    def __init__(self, status_callback):
        self.board_shim = None
        self.sampling_rate = None
        self.asr = None
        self.session_active = True  # Kontrollvariable als Attribut
        self.status_callback = status_callback

    def connect_board(self):
        BoardShim.enable_dev_board_logger()
        parser = argparse.ArgumentParser()
        parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
        parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                            required=False, default=BoardIds.SYNTHETIC_BOARD)
        args = parser.parse_args(['--serial-port', 'COM3', '--board-id', '-1']) # Set board to -1 for synthetic data; 2 for cyton+daisy

        params = BrainFlowInputParams()
        params.serial_port = args.serial_port
        self.board_shim = BoardShim(args.board_id, params)
        self.board_shim.prepare_session()

        # Set the sampling rate after the board is connected
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_shim.board_id)

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

                        # Speichere die berechneten Werte und den Zeitstempel direkt in die HDF5-Datei
                        self.save_eeg_data_as_hdf5(HDF5_FILENAME, timestamp, theta_power, alpha_power, beta_power)

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

    def save_eeg_data_as_hdf5(self, filename, timestamp, theta_power, alpha_power, beta_power):
        """
        Speichert die EEG-Daten als HDF5-Datei.
        """
        # Neue Daten hinzufügen
        with h5py.File(filename, 'a') as h5_file:
            eeg_dataset = h5_file['EEG_data']
            new_index = eeg_dataset.shape[0]

            eeg_dataset.resize((new_index + 1,))
            eeg_dataset[new_index] = (timestamp, theta_power, alpha_power, beta_power)

        self.status_callback(f"EEG Data saved to {filename}")

async def process_messages(eeg_mon: EEGMonitoring, status_callback):
    while True:
        message = await client.message_queue.get()  # Nachricht aus der Warteschlange holen
        if message is None:
            break
        status_callback(f"Processing message: {message}")

        parsed_message = json.loads(message)
        action = parsed_message.get("action")

        if action == "start_baseline_recording":
            await eeg_mon.record_asr_baseline()
            status_callback("Finished ASR recording and training.")
        elif action == "start_recording":
            status_callback("Started recording.")
            await asyncio.gather(
                hr_mon.monitor_heart_rate(),
                eeg_mon.monitor_cognitive_load(client),
                app.keyboard_listener()  # Startet den Keyboard Listener als Teil der Aufzeichnung
            )
        elif action == "stop_recording":
            # Stop both HR and EEG monitoring
            eeg_mon.session_active = False  # Beende die while-Schleife in monitor_cognitive_load
            await hr_mon.release_hr_device()
            eeg_mon.release_board()
            status_callback("Stopped HR and EEG Monitoring")

class MonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EEG & HR Monitoring")

        # Registriere die Methode, die ausgeführt wird, wenn das Fenster geschlossen wird
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        # Labels and Entries for participant ID, IP Address, HR Device Name Part
        ttk.Label(root, text="Participant ID:").grid(column=0, row=0, padx=10, pady=10)
        self.participant_id_entry = ttk.Entry(root)
        self.participant_id_entry.grid(column=1, row=0, padx=10, pady=10)
        self.participant_id_entry.insert(0, "12345")  # Voreintrag für IP-Adresse

        ttk.Label(root, text="IP Address:").grid(column=0, row=1, padx=10, pady=10)
        self.ip_address_entry = ttk.Entry(root)
        self.ip_address_entry.grid(column=1, row=1, padx=10, pady=10)
        self.ip_address_entry.insert(0, "127.0.0.1:8000")  # Voreintrag für IP-Adresse

        ttk.Label(root, text="HR Device Name:").grid(column=0, row=2, padx=10, pady=10)
        self.hr_device_name_entry = ttk.Entry(root)
        self.hr_device_name_entry.grid(column=1, row=2, padx=10, pady=10)
        self.hr_device_name_entry.insert(0, "78E6F727")  # Voreintrag für HR-Gerätenamen

        # Status labels
        self.status_label = ttk.Label(root, text="Status: Not connected")
        self.status_label.grid(column=0, row=8, columnspan=2, padx=10, pady=10)

        # Buttons for connection

        self.connect_eeg_button = ttk.Button(root, text="Connect EEG", command=self.connect_eeg)
        self.connect_eeg_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

        self.create_h5_button = ttk.Button(root, text="Create HDF5 File", command=self.create_h5_file)
        self.create_h5_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10)

        # Labels for connection status (witch checkmark)
        self.hr_status_icon = tk.Label(root, text="")  # Initially empty
        self.hr_status_icon.grid(column=1, row=3, padx=10, pady=10)

        self.eeg_status_icon = tk.Label(root, text="")  # Initially empty
        self.eeg_status_icon.grid(column=1, row=4, padx=10, pady=10)

        self.ws_status_icon = tk.Label(root, text="")  # Initially empty
        self.ws_status_icon.grid(column=1, row=5, padx=10, pady=10)

        self.data_status_icon = tk.Label(root, text="")  # Initially empty
        self.data_status_icon.grid(column=1, row=6, padx=10, pady=10)

        # Add Buttons for Actions
        self.start_baseline_button = ttk.Button(root, text="Start Baseline Recording", command=lambda: asyncio.run(self.start_baseline()))

        self.start_baseline_button.grid(column=0, row=7, columnspan=2, padx=10, pady=5)

        self.start_recording_button = ttk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_recording_button.grid(column=0, row=8, columnspan=2, padx=10, pady=5)

        self.stop_recording_button = ttk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_recording_button.grid(column=0, row=9, columnspan=2, padx=10, pady=5)


        # Monitoring attributes
        self.eeg_monitor = None
        self.hr_monitor = None
        self.websocket_client = None

        # Initialize asyncio loop
        self.loop = asyncio.get_event_loop()

    def start_baseline(self):
        asyncio.run(self._start_baseline())

    async def _start_baseline(self):
        await eeg_mon.record_asr_baseline()
        status_callback("Finished ASR recording and training.")


    async def start_recording(self):
        """Start the recording process."""
        if self.eeg_monitor:
            await asyncio.gather(
                self.eeg_monitor.monitor_cognitive_load(None),  # Replace None with your client if necessary
                self.keyboard_listener()
            )
        else:
            self.update_status("HR or EEG Monitor is not connected.")

    def stop_recording(self):
        """Stop the recording process."""
        if self.eeg_monitor:
            self.eeg_monitor.session_active = False
            self.eeg_monitor.release_board()
        if self.hr_monitor:
            self.loop.create_task(self.hr_monitor.release_hr_device())
        self.update_status("Stopped HR and EEG Monitoring.")

    async def keyboard_listener(self):
        """
        Startet den Keyboard Listener und speichert die Timestamps von Tastendrücken in die HDF5-Datei.
        """

        def key_handler(event):
            if event.name == 'space':
                timestamp = time.time()
                with h5py.File(HDF5_FILENAME, 'a') as h5_file:
                    keypress_dataset = h5_file['Keypress_data']
                    new_index = keypress_dataset.shape[0]
                    keypress_dataset.resize((new_index + 1,))
                    keypress_dataset[new_index] = (timestamp, event.name.encode('utf-8'))
                self.update_status(f"Keypress recorded: {event.name} at {timestamp}")

        keyboard.on_press(key_handler)
        self.update_status("Keyboard listener started. Press the button to log a keypress.")

        try:
            while True:
                await asyncio.sleep(1)
        finally:
            keyboard.unhook_all()
            self.update_status("Keyboard listener stopped.")

    def connect_eeg(self):
        self.eeg_monitor = EEGMonitoring(self.update_status)
        try:
            self.eeg_monitor.connect_board()
            self.update_status("EEG Board connected successfully")
            self.root.after(0, self.eeg_status_icon.config, {"text": "✓", "fg": "green"})
        except Exception as e:
            self.update_status(f"EEG Board connection failed: {e}")


    def create_h5_file(self):
        participant_id = self.participant_id_entry.get()
        if not participant_id:
            self.update_status("Participant ID is required to create HDF5 file")
            return

        global HDF5_FILENAME
        HDF5_FILENAME = f"data_{participant_id}.h5"
        if not os.path.exists(HDF5_FILENAME):
            with h5py.File(HDF5_FILENAME, 'w') as h5_file:
                eeg_dtype = np.dtype([('timestamp', 'f8'), ('theta', 'f8'), ('alpha', 'f8'), ('beta', 'f8')])
                hr_dtype = np.dtype([('timestamp', 'f8'), ('rr_interval', 'f8'), ('heart_rate', 'f8'), ('raw', 'f8')])
                keypress_dtype = np.dtype([('timestamp', 'f8'), ('key', 'S10')])
                h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
                h5_file.create_dataset('HR_data', shape=(0,), maxshape=(None,), dtype=hr_dtype)
                h5_file.create_dataset('Keypress_data', shape=(0,), maxshape=(None,), dtype=keypress_dtype)
            self.update_status("HDF5 file created successfully")
            self.root.after(0, self.data_status_icon.config, {"text": "✓", "fg": "green"})
        else:
            self.update_status("HDF5 file already exists")
            self.root.after(0, self.data_status_icon.config, {"text": "✓", "fg": "green"})

    def update_status(self, message):
        self.root.after(0, self.status_label.config, {"text": message})

    def close_app(self):
        async def close_all():
            try:
                # Schließe die EEG-Verbindung
                if self.eeg_monitor:
                    self.eeg_monitor.release_board()
                    print("Released EEG Board.")

                # Schließe die HR-Verbindung und die WebSocket-Verbindung
                tasks = []

                if self.hr_monitor:
                    tasks.append(self.hr_monitor.release_hr_device())

                if self.websocket_client:
                    tasks.append(self.websocket_client.close_websocket_client())

                # Führe alle asynchronen Aufgaben aus und warte auf den Abschluss
                if tasks:
                    await asyncio.gather(*tasks)

                print("All connections closed.")

            except Exception as e:
                print(f"Error during close: {e}")

            finally:
                # Schließe das Fenster
                self.root.destroy()

        # Starte die asynchrone Schließfunktion als Task im Event Loop
        self.loop.create_task(close_all())

    def run(self):
        # Periodically call the asyncio event loop to keep the GUI responsive
        self.root.after(100, self._run_asyncio_loop)
        self.root.mainloop()

    def _run_asyncio_loop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.loop.run_forever()
        self.root.after(100, self._run_asyncio_loop)

    

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitoringApp(root)
    app.run()