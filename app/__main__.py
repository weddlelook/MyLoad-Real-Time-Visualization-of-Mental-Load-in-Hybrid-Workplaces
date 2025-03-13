import sys
from app.controller.Controller2 import Controller
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.next_page("start")
    app.exec()
    app.deleteLater()

if __name__ == "__main__":
    main()