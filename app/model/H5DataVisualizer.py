import h5py
import matplotlib.pyplot as plt
import os

"""
This class contains function for plotting a single session or multiple ones, which is important for the retrospective
"""

class H5DataVisualizer:

    def __init__(self, directory='h5_session_files'):
        self.directory = directory

    def list_sessions(self):
        # Gibt eine Liste aller HDF5-Dateien im Verzeichnis zurück
        result = []
        for f in os.listdir(self.directory):
            if f.endswith(".h5"):
                result.append(f)
        return result

    def plot_h5_data(self, file_name):

        file_path = os.path.join(self.directory, file_name) # Speichert die konkrete File aus dem h5 Ordner
        try:
            with h5py.File(file_path, 'r') as file:

                file = file['EEG_data']
                timestamps = file['timestamp'][:] # Zeitdaten
                cognitive_load = file['cognitive_load'][:] # Cognitive Load

            # Plot erstellen
            plt.figure(figsize=(10, 6))
            plt.plot(timestamps, cognitive_load, label=f'Session: {file_name}', color='blue')
            plt.title('Cognitive Load über die Zeit')
            plt.xlabel('Zeit (s)')
            plt.ylabel('Cognitive Load')
            plt.grid(True)
            plt.legend()
            plt.show()
        except Exception as e:
            print(f"Fehler beim Plotten der H5-Daten: {e}")


    def plot_multiple_sessions(self, filenames):
        # Mehrere Sessions plotten
        plt.figure(figsize=(10, 6))
        try:
            for filename in filenames:
                filepath = os.path.join(self.directory, filename)
                with h5py.File(filepath, 'r') as h5file:
                    time = h5file['timestamps'][:]  # Zeitdaten
                    load = h5file['cognitive_load'][:]  # Cognitive Load

                # Jede Session hinzufügen
                plt.plot(time, load, label=f"Session: {filename}")

            plt.xlabel("Zeit (s)")
            plt.ylabel("Cognitive Load")
            plt.title('Cognitive Load über die Zeit')
            plt.legend()
            plt.show()
        except Exception as e:
            print(f"Fehler beim Plotten der H5-Daten: {e}")