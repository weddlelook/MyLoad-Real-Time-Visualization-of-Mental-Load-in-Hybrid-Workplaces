from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
import os
import h5py
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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
        self.plot_button = QPushButton("Ausgewählte Sessions plotten")
        self.plot_button.clicked.connect(self.plot_sessions)
        layout.addWidget(self.plot_button)

        # Matplotlib-Canvas für das Plotten
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Lade die verfügbaren Sessions
        self.load_sessions()

        self.back_button = QPushButton("Zurück zur Startseite")
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignRight)


        self.setStyleSheet("""
                    QPushButton {
                        background-color: #F4F4F4;  /* grey-ish background */
                        color: black;              /* black text */
                        border: 2px solid #000000; /* black border */
                        border-radius: 10px;       /* Rounded corners */
                        padding: 10px;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #D3D3D3; /* Darker grey on hover */
                    }
                    QPushButton:pressed {
                        background-color: #BEBEBE; /* Even darker grey when pressed */
                    }""")

    def load_sessions(self):
        """Lade alle .h5-Dateien aus dem Session-Ordner."""
        self.session_list.clear()
        if os.path.exists(self.session_folder):
            for file in os.listdir(self.session_folder):
                if file.endswith(".h5"):
                    self.session_list.addItem(file)

    def plot_sessions(self):
        """Plotte die ausgewählten Sessions mit Zeitstempeln relativ zum Startzeitpunkt."""
        selected_files = [item.text() for item in self.session_list.selectedItems()]
        if not selected_files:
            print("Keine Sessions ausgewählt.")
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        for file in selected_files:
            file_path = os.path.join(self.session_folder, file)
            try:
                with h5py.File(file_path, 'r') as h5_file:
                    eeg_data = h5_file['EEG_data'][:]
                    timestamps = eeg_data['timestamp']
                    cognitive_load = eeg_data['cognitive_load']

                    # Setze die Zeitstempel relativ zum Startzeitpunkt
                    timestamps_rel = timestamps - timestamps[0]  # Startzeitpunkt abziehen
                    ax.plot(timestamps_rel, cognitive_load, label=file)
            except Exception as e:
                print(f"Fehler beim Lesen der Datei {file}: {e}")

        ax.set_xlabel("Zeit (s)")
        ax.set_ylabel("Cognitive Load")
        ax.legend()
        ax.grid(True)
        self.canvas.draw()