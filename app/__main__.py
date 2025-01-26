import sys
from app.controller.controller import Controller
from PyQt6.QtWidgets import QApplication
from H5DataVisualizer import plot_h5_data

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.landing_page()
    app.exec()
    app.deleteLater()

if __name__ == "__main__":
    main()