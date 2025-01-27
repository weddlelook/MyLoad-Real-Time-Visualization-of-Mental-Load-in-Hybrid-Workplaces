from PyQt6.QtWidgets import QStackedLayout, QMainWindow, QVBoxLayout, QWidget
from app.view.startWidget import StartWidget
from app.view.plotWidget import EEGPlotWidget
from app.view.baselinePage import BaselineWidget
from app.view.maxtestPage import MaxtestPage
from app.view.settingsPage import SettingsWidget
from app.view.retrospectivePage import RetrospektivePage

class RootWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.main_window = MainWidget()
        self.setCentralWidget(self.main_window)
        self.show()

class MainWidget(QWidget):

    """
    This class represents the main Window of this application.
    It holds two child-Widgets:
    > A stack holding all Stages of the Lifecycle
    > A Settings - Widget
    that can be switched with the provided methods
    """

    def __init__(self):
        super().__init__()

        # Main layout container
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Setting up Settings
        self.settings = SettingsWidget()

        # Setting up Stack
        self.stack = QWidget()
        self.stack_layout = QStackedLayout()
        self.stack.setLayout(self.stack_layout)

        # Adding to main Widget
        self.main_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.settings)

        # Dict for all registered pages
        self.pages = {}

        # Registering all pages 
        # NOTE: We could decide to not register all pages here, but instead register them 
        #       as we go along in the application lifecycle, but for now, we will register them all here
        self._register_page(StartWidget(), "start")
        self._register_page(EEGPlotWidget(), "plot")
        self._register_page(BaselineWidget(), "baseline")
        self._register_page(MaxtestPage(), "maxtest")
        self._register_page(RetrospektivePage("h5_session_files"), "retrospective")


        self.settings.hide()

    def _register_page(self, child: QWidget, page_name: str):
        """Registers a page with the main window."""
        self.stack_layout.addWidget(child)
        self.pages[page_name] = child

    def set_page(self, page_name:str) -> QWidget:
        """
        Sets the current index of the main window to the page with the given name.
        Returns the Widget.
        """
        try:
            widget = self.pages[page_name]
            widget_index = self.stack_layout.indexOf(widget)
            self.stack_layout.setCurrentIndex(widget_index)
            return widget
        except KeyError as e: 
            print(f"Error during page change: {e}")
            return None

    def open_settings(self):
        self.settings.show()
        self.stack.hide()

    def close_settings(self):
        self.settings.hide()
        self.stack.show()
