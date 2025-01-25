import h5py
import matplotlib.pyplot as plt



def plot_h5_data(file_path):
    try:
        with h5py.File(file_path, 'r') as file:

            file = file['EEG_data']
            # Daten laden (Passe die Keys an die Struktur deiner Datei an)
            timestamps = file['timestamp'][:]
            cognitive_load = file['cognitive_load'][:]

        # Plot erstellen
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, cognitive_load, label='Cognitive Load', color='blue')
        plt.title('Cognitive Load über die Zeit')
        plt.xlabel('Zeit (s)')
        plt.ylabel('Cognitive Load')
        plt.grid(True)
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"Fehler beim Plotten der H5-Daten: {e}")