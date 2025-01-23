import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg

class EEGPlotWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEG Power Live Plot")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.theta_curve = self.plot_widget.plot(pen='r', name="Theta Power")
        self.alpha_curve = self.plot_widget.plot(pen='g', name="Alpha Power")
        self.beta_curve = self.plot_widget.plot(pen='b', name="Beta Power")
        self.cl_curve = self.plot_widget.plot(pen='m', name="Cognitive Load")

        self.theta_data = []
        self.alpha_data = []
        self.beta_data = []
        self.cl_data = []
        self.timestamps = []

    def update_plot(self, powers):
        self.timestamps.append(powers['timestamp'])
        self.theta_data.append(powers['theta_power'])
        self.alpha_data.append(powers['alpha_power'])
        self.beta_data.append(powers['beta_power'])
        self.cl_data.append(powers['cognitive_load'])

        self.theta_curve.setData(self.timestamps, self.theta_data)
        self.alpha_curve.setData(self.timestamps, self.alpha_data)
        self.beta_curve.setData(self.timestamps, self.beta_data)
        self.cl_curve.setData(self.timestamps, self.cl_data)