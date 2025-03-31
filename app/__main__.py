import sys
from app.controller.controller import Controller
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.next_page("start")
    app.exec()
    controller.deleteLater()
    app.deleteLater()


if __name__ == "__main__":
    main()
