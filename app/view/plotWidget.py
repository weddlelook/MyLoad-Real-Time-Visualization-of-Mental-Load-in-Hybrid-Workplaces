import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import pyqtgraph as pg

class EEGPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEG Power Live Plot")
        self.layout = QVBoxLayout()

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)

        self.theta_curve = self.plot_widget.plot(pen='r', name="Theta Power")
        self.alpha_curve = self.plot_widget.plot(pen='g', name="Alpha Power")
        self.beta_curve = self.plot_widget.plot(pen='b', name="Beta Power")

        self.theta_data = []
        self.alpha_data = []
        self.beta_data = []
        self.timestamps = []


    def update_plot(self, powers):
        self.timestamps.append(powers['timestamp'])
        self.theta_data.append(powers['theta_power'])
        self.alpha_data.append(powers['alpha_power'])
        self.beta_data.append(powers['beta_power'])

        self.theta_curve.setData(self.timestamps, self.theta_data)
        self.alpha_curve.setData(self.timestamps, self.alpha_data)
        self.beta_curve.setData(self.timestamps, self.beta_data)