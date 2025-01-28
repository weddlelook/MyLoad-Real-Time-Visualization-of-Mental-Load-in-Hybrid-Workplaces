from PyQt6.QtWidgets import QStackedLayout, QMainWindow, QVBoxLayout, QWidget
from app.view.startWidget import StartWidget
from app.view.plotWidget import EEGPlotWidget
from app.view.baselinePage import BaselineWidget
from app.view.maxtestPage import MaxtestPage
from app.view.settingsPage import SettingsWidget
from app.view.startBaselinePage import StartBaselinePage

class RootWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.setWindowTitle("")
        self.settings = settings
        self.main_window = MainWidget()
        self.setCentralWidget(self.main_window)
        self.apply_stylesheet()
        self.show()

    def apply_stylesheet(self):
        if self.settings["lightMode"] == 1:
            file_path = "app/view/styles/style_light.qss"
        elif self.settings["darkMode"] == 1:
            file_path = "app/view/styles/style_dark.qss"
        try:
            with open(file_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: Stylesheet '{file_path}' not found.")


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main window layout, which will be a stacked layout
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        # Dict for all registered pages
        self.pages = {}

        # Registering all pages 
        # NOTE: We could decide to not register all pages here, but instead register them 
        #       as we go along in the application lifecycle, but for now, we will register them all here
        self.register_page(StartWidget(), "start")
        self.register_page(EEGPlotWidget(), "plot")
        self.register_page(BaselineWidget(), "baseline")
        self.register_page(MaxtestPage(), "maxtest")
        self.register_page(SettingsWidget(), "settings")
        self.register_page(StartBaselinePage(), "baselineStartPage")


    def register_page(self, child: QWidget, page_name: str):
        """Registers a page with the main window."""
        self.layout.addWidget(child)
        self.pages[page_name] = child
