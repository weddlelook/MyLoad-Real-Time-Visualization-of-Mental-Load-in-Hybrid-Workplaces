import sys
from controller.controller import Controller
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.landing_page()
    app.exec()
    app.deleteLater()

if __name__ == "__main__":
    main()