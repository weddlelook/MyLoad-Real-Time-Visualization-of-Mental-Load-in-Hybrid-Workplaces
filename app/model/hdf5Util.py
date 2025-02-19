from .constants import * 
import os
import h5py
from datetime import datetime
import numpy as np

class hdf5File:

      def __init__(self, users_session_name:str):
            self.filename = self._create_h5_file(users_session_name)

      def save_eeg_data_as_hdf5(self, powers):     
            """
            Speichert die EEG-Daten als HDF5-Datei.
            TODO: Depending on where we implement the calculation of CL out of the powers, we might want to move this function to the controller or implement the calculation of CL here
                  The file layout also needs adjustment for the CL if we also store that in the file
            """
            timestamp, theta_power, alpha_power, beta_power, cognitive_load = (
                  powers["timestamp"],
                  powers["theta_power"],
                  powers["alpha_power"],
                  powers["beta_power"],
                  powers["cognitive_load"],
            )

            # Neue Daten hinzufügen
            with h5py.File(self.filename, 'a') as h5_file:
                  eeg_dataset = h5_file['EEG_data']
                  new_index = eeg_dataset.shape[0]

                  eeg_dataset.resize((new_index + 1,))
                  eeg_dataset[new_index] = (timestamp, theta_power, alpha_power, beta_power, cognitive_load)

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
                        eeg_dtype = np.dtype([('timestamp', 'f8'), ('theta', 'f8'), ('alpha', 'f8'), ('beta', 'f8'),
                                          ('cognitive_load', 'f8')])
                        h5_file.create_dataset('EEG_data', shape=(0,), maxshape=(None,), dtype=eeg_dtype)
                        print(f"HDF5 file created successfully: {HDF5_FILENAME}")
            return HDF5_FILENAME

      @staticmethod
      def plot_file(filename:str):
            pass