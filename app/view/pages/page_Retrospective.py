from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
import os
import h5py
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import time
from datetime import datetime, timedelta
import mplcursors







"""
FYI: Falls Ihr h5 sessions plottet achtet darauf dass diese auch tatsächlich CL Daten vom Monitoring haben. 
     Dh nach dem Baseline messen kurz synthetische CL daten generiert wurden für die h5. Ansonsten ist der Plot leer. 
"""


class RetrospectivePage(QWidget):
    def __init__(self, session_folder):
        super().__init__()
        self.session_folder = session_folder
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Liste der Sessions
        self.session_list = QListWidget()
        self.session_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)  # Mehrfachauswahl aktivieren
        layout.addWidget(self.session_list)

        # Button zum Plotten
        self.plot_button = QPushButton("Plot Sessions")
        self.plot_button.clicked.connect(self._plot_sessions)
        layout.addWidget(self.plot_button)

        # Matplotlib-Canvas für das Plotten
        self.figure = Figure(facecolor="#F8F8FF", edgecolor="#444444")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Lade die verfügbaren Sessions
        self.load_sessions()

        self.back_button = QPushButton("Back to Homepage")
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignRight)


    def load_sessions(self):
        """Lade alle .h5-Dateien aus dem Session-Ordner."""
        self.session_list.clear()
        if os.path.exists(self.session_folder):
            files = [f for f in os.listdir(self.session_folder) if f.endswith(".h5")]

            def extract_index(file_name):
                file_name = str(file_name)
                index = file_name.split("__")[0].strip()
                return int(index)

            files.sort(key=extract_index, reverse=True)
            for file in files:
                self.session_list.addItem(file)

    def _extract_start_time(self, filename):
        # Extrahiere den Zeitstempel aus dem Dateinamen
        time_str = filename.split("__")[-1].split(".")[0]  # z. B. "07-06-37_28-01-2025"
        return datetime.strptime(time_str, "%H-%M-%S_%d-%m-%Y")

    def _convert_timestamps(self, start_time, timestamps):
        # Addiere die Sekunden zum Startzeitpunkt. Bsp Startzeitpunkt: 15:00:00, falls die Session 1min = 60s ging,
        # werden 60 verschiedene timestamps erstellt mit 15:00:00, 15:00:01 etc
        converted_timestamps = []
        for seconds in range(len(timestamps)):
            new_timestamp = start_time + timedelta(seconds=seconds)
            if new_timestamp not in converted_timestamps:

                converted_timestamps.append(start_time + timedelta(seconds=seconds))
        return converted_timestamps

    def _plot_sessions(self):
        """
        Plottet die ausgewählten Sessions. Wählt man nur eine Session aus, so sieht man auf der x -Achse den
        zeitlichen Verlauf der Session mit Uhrzeiten.
        Werden mehrere ausgewählt, so werden die Zeiten normalisiert und alle Verläufe fangen bei 0 an.
        """
        selected_files = [item.text() for item in self.session_list.selectedItems()]
        if not selected_files:
            print("Keine Sessions ausgewählt.")
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        show_concrete_time = len(selected_files) == 1

        for file in selected_files:
            file_path = os.path.join(self.session_folder, file)
            try:
                with h5py.File(file_path, 'r') as h5_file:
                    eeg_data = h5_file['EEG_data'][:]
                    timestamps = eeg_data['timestamp']
                    cognitive_load_score = eeg_data['load_score']

                    #Falls nur eine Session geplottet wird
                    if show_concrete_time:
                        # Extrahiere den Startzeitpunkt aus dem Dateinamen
                        start_time = self._extract_start_time(file)
                        print("start zeit: " + str(start_time))
                        # Konvertiere die Zeitstempel in "Stunde:Minute"
                        time_labels = self._convert_timestamps(start_time, timestamps)

                        ax.plot(time_labels, cognitive_load_score, label=file)
                        ax.legend(loc="upper right")

                        # Lade und plotte Marker
                        if 'markers' in h5_file:
                            markers = h5_file['markers'][:]
                            marker_times = [start_time + timedelta(seconds=int(m[0] - timestamps[0])) for m in markers]
                            marker_descriptions = [m[1].decode() for m in markers]

                            marker_cl_values = [
                                cognitive_load_score[np.argmin(np.abs(timestamps - m[0]))] for m in markers
                            ]

                            scatter = ax.scatter(marker_times, marker_cl_values, color='red', label='Kommentare',
                                                 marker='o', s=50)
                            cursor = mplcursors.cursor(scatter, hover=True)

                            @cursor.connect("add")
                            def on_hover(sel):
                                sel.annotation.set_text(marker_descriptions[sel.index])


                            #Falls mehrere Sessions geplottet werden sollen
                    else:
                        # Setze die Zeitstempel relativ zum Startzeitpunkt
                        timestamps_rel = timestamps - timestamps[0]  # Startzeitpunkt abziehen
                        ax.plot(timestamps_rel, cognitive_load_score, label=file)
            except Exception as e:
                print(f"Fehler beim Lesen der Datei {file}: {e}")

        ax.set_xlabel("Zeit (Stunde:Minute)" if len(selected_files) == 1 else "Zeit (s)")
        ax.set_ylabel("Cognitive Load")
        ax.legend(loc="upper left", bbox_to_anchor=(-0.16, 1.15), borderaxespad=0.)
        ax.grid(True)
        self.canvas.draw()