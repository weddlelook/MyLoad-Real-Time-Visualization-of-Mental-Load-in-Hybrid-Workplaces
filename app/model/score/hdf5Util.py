from ..constants import * 
import os
import h5py
from datetime import datetime
import numpy as np

class hdf5File:

      def __init__(self, users_session_name:str):
            self.filename = self._create_h5_file(users_session_name)

      def save_eeg_data_as_hdf5(self, powers):     
            timestamp, theta_power, alpha_power, beta_power, cognitive_load, load_score = (
                  powers["timestamp"],
                  powers["theta_power"],
                  powers["alpha_power"],
                  powers["beta_power"],
                  powers["cognitive_load"],
                  powers["load_score"]
            )

            # Neue Daten hinzufügen
            with h5py.File(self.filename, 'a') as h5_file:
                  eeg_dataset = h5_file['EEG_data']
                  new_index = eeg_dataset.shape[0]

                  eeg_dataset.resize((new_index + 1,))
                  eeg_dataset[new_index] = (timestamp, theta_power, alpha_power, beta_power, cognitive_load, load_score)

      def save_marker(self, timestamp, description):
            with h5py.File(self.filename, 'a') as h5_file:
                  description = str(description)
                  markers = h5_file['markers']
                  new_marker = np.array([(timestamp, description.encode())], dtype=markers.dtype)
                  markers.resize((markers.shape[0] + 1,))
                  markers[-1] = new_marker[0]
                  # Print all markers directly
                  print("Alle Marker in der .h5-Datei:")
                  for marker in markers:
                        print(f"Zeitstempel: {marker[0]}, Beschreibung: {marker[1].decode()}")

      def set_min(self, min_value: float):
            with h5py.File(self.filename, 'a') as h5_file:
                  h5_file.attrs['min'] = min_value  # Store min as an attribute

      def set_max(self, max_value: float):
            with h5py.File(self.filename, 'a') as h5_file:
                  h5_file.attrs['max'] = max_value  # Store max as an attribute

      def get_h5_file(fileName:str) -> float:
            if not fileName.endswith(".h5"):
                  fileName += ".h5"

            # Lese den Standard-Ordnerpfad aus den Konstanten
            folder_path = getAbsPath(HDF5_FOLDER_PATH)

            # Überprüfe, ob der Ordner existiert
            if not os.path.exists(folder_path):
                  print(f"Ordner {folder_path} existiert nicht.")
                  return None

            # Durchsuche den Ordner nach der Datei
            for file in os.listdir(folder_path):
                  if file == fileName:
                        return os.path.join(folder_path, file)

            # Datei nicht gefunden
            print(f"Datei {fileName} nicht gefunden in {folder_path}.")
            return None

      def get_min_value(file_path):
            try:
                  with h5py.File(file_path, 'r') as h5_file:
                        min_value = h5_file.attrs.get('min', None)
                        return min_value
            except FileNotFoundError:
                  print(f"Fehler beim Lesen der Datei {file_path}: {e}")
                  return None

      def get_max_value(file_path):
            try:
                  with h5py.File(file_path, 'r') as h5_file:
                        max_value = h5_file.attrs.get('max', None)
                        print(max_value)
                        return max_value
            except FileNotFoundError:
                  print(f"Fehler beim Lesen der Datei {file_path}: {e}")
                  return None


      def _create_h5_file(self, users_session_name:str):
            # Ordner erstellen, falls er nicht existiert
            folder_path = getAbsPath(HDF5_FOLDER_PATH)
            if not os.path.exists(folder_path):
                  os.makedirs(folder_path)

            # Variable welche den Sessions noch eine Nummer gibt, damit diese nummeriert bleiben
            count_of_sessions = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]) + 1

            timestamp = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
            HDF5_FILENAME = os.path.join(folder_path, f"{count_of_sessions}__{users_session_name}__{timestamp}.h5")

            # Datei erstellen, falls sie nicht existiert
            if not os.path.exists(HDF5_FILENAME):
                  with h5py.File(HDF5_FILENAME, 'w') as h5_file:
                        #Dataset for eeg data
                        eeg_dtype = np.dtype([
                              ('timestamp', 'f8'), 
                              ('theta', 'f8'), 
                              ('alpha', 'f8'), 
                              ('beta', 'f8'),
                              ('cognitive_load', 'f8'),
                              ('load_score', 'f8')])
                        h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
                        h5_file.attrs['min'] = np.nan
                        h5_file.attrs['max'] = np.nan

                        #Dataset for user comments
                        str_dtype = h5py.string_dtype('utf-8')
                        marker_dtype = np.dtype(
                              [('timestamp', 'f8'),
                               ('description', str_dtype)])
                        h5_file.create_dataset('markers', shape=(0,), maxshape=(None,), dtype=marker_dtype)

                        print(f"HDF5 file created successfully: {HDF5_FILENAME}")
            return HDF5_FILENAME

      @staticmethod
      def plot_file(filename: str):
            with h5py.File(filename, 'r') as h5_file:
                  eeg_data = h5_file['EEG_data']
                  timestamps = [int(timestamp) for timestamp in eeg_data['timestamp']]
                  load_score = eeg_data['load_score']
                  markers = h5_file['markers']
                  timestamps_marker = [int(timestamp) for timestamp in markers['timestamp']]
                  y_marker = np.zeros(len(timestamps_marker))
                  descriptions = markers['description']

                  # Initialize a list to collect the modified timestamps and load scores
                  modified_timestamps = []
                  modified_load_score = []
                  
                  # Pointer to go through the marker timestamps
                  marker_idx = 0

                  # Iterate through the timestamps and load scores
                  for idx, (timestamp, score) in enumerate(zip(timestamps, load_score)):
                        # Check for gap and add missing timestamps
                        if idx > 0 and timestamp > timestamps[idx - 1] + 1:
                              for missing_time in range(timestamps[idx - 1] + 1, timestamp):
                                    modified_timestamps.append(missing_time)
                                    modified_load_score.append(np.nan)  # Set NaN for missing load score
                                    
                                    if marker_idx < len(timestamps_marker) and missing_time == timestamps_marker[marker_idx]:

                                          y_marker[marker_idx] = np.nan
                                          marker_idx += 1

                        # Now add the current timestamp and load score
                        modified_timestamps.append(timestamp)
                        modified_load_score.append(score)
                        
                        if marker_idx < len(timestamps_marker) and timestamp == timestamps_marker[marker_idx]:
                              y_marker[marker_idx] = score
                              marker_idx += 1

                  return np.array(modified_timestamps), np.array(modified_load_score), timestamps_marker, y_marker, descriptions