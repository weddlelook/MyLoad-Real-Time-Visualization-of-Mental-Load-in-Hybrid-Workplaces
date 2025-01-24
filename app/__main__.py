import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from app.H5DataVisualizer import plot_h5_data
from view.rootWindow import RootWindow
from controller.controller import Controller

def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    gui = RootWindow()
    controller = Controller(gui)
    print("Controller initialized")
    gui.show()


    with loop:  # Run the event loop
        loop.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
