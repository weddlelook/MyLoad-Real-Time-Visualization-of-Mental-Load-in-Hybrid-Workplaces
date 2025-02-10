import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
import pyqtgraph as pg
from PyQt6.QtGui import QFont

class EEGPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEG Power Live Plot")
        self.layout = QVBoxLayout()

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        #self.setLayout(self.layout)

        self.theta_curve = self.plot_widget.plot(pen='r', name="Theta Power")
        self.alpha_curve = self.plot_widget.plot(pen='g', name="Alpha Power")
        self.beta_curve = self.plot_widget.plot(pen='b', name="Beta Power")

        self.theta_data = []
        self.alpha_data = []
        self.beta_data = []
        self.timestamps = []

        self.score = 0
        self.label = QLabel()
        self.label.setText(str(self.score))

        # Text größer machen
        font = QFont("Arial", 15)  # Schriftart und Schriftgröße
        self.label.setFont(font)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def updateScore(self, score):
        print("widget")
        self.label.setText(str(score))


    def update_plot(self, powers):
        self.timestamps.append(powers['timestamp'])
        self.theta_data.append(powers['theta_power'])
        self.alpha_data.append(powers['alpha_power'])
        self.beta_data.append(powers['beta_power'])

        self.theta_curve.setData(self.timestamps, self.theta_data)
        self.alpha_curve.setData(self.timestamps, self.alpha_data)
        self.beta_curve.setData(self.timestamps, self.beta_data)