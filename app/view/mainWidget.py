from PyQt6.QtWidgets import QStackedLayout, QVBoxLayout, QWidget

# Custom pages import
from app.view.startWidget import StartWidget
from app.view.plotWidget import EEGPlotWidget
from app.view.baselinePage import BaselineWidget
from app.view.maxtestPage import MaxtestPage
from app.view.settingsPage import SettingsWidget
from app.view.startBaselinePage import StartBaselinePage
from app.view.retrospectivePage import RetrospectivePage
from app.view.resultsPage import ResultsPage
from app.view.startMaxtestPage import StartMaxTestPage

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

        # Adding Settings and Stack to main Widget
        self.main_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.settings)

        # Dict for all registered pages
        self.pages = {}
        #Previous page in stack
        self.previous_page_name = None

        # Registering all pages 
        # NOTE: We could decide to not register all pages here, but instead register them 
        #       as we go along in the application lifecycle, but for now, we will register them all here
        self._register_page(StartWidget(), "start")
        self._register_page(EEGPlotWidget(), "plot")
        self._register_page(BaselineWidget(), "baseline")
        self._register_page(StartBaselinePage(), "baselineStartPage")
        self._register_page(MaxtestPage(), "maxtest")
        self._register_page(RetrospectivePage("h5_session_files"), "retrospective")
        self._register_page(ResultsPage(), "result")
        self._register_page(StartMaxTestPage(), "startmaxtest")


        self.settings.hide()

    def _register_page(self, child: QWidget, page_name: str):
        """Registers a page with the main window."""
        self.stack_layout.addWidget(child)
        self.pages[page_name] = child

    def set_page(self, page_name: str) -> QWidget:
        """
        Sets the current index of the main window to the page with the given name.
        And updates the previous widgets name
        Returns the Widget.
        """
        current_page_name = self._get_name_of_widget()
        self.previous_page_name = current_page_name
        try:
            widget = self.pages[page_name]
            widget_index = self.stack_layout.indexOf(widget)
            self.stack_layout.setCurrentIndex(widget_index)
            return widget
        except KeyError as e:
            print(f"Error during page change: {e}")
            return None

    def toggle_settings(self):
        """
        Toggels the main window between showing the normal Stack
        and the settings
        """
        if self.settings.isVisible():
            self.settings.hide()
            self.stack.show()
        else:
            self.stack.hide()
            self.settings.show()

    def toggle_retrospective(self):
        """
        Toggels the main window between retrospective page and previous page
        """
        current_widget = self._get_name_of_widget()
        if current_widget != "retrospective":
            if self.settings.isVisible():
                self.settings.hide()
                self.stack.show()
            widget = self.set_page("retrospective")
            widget.back_button.clicked.connect(lambda: self.set_page(self.previous_page_name))
        else:
            self.set_page(self.previous_page_name)

    def _get_name_of_widget(self, get_widget=None):
        """
        Gets the name of the given widget in pages
        if no widget is given default it returns the current widgets name
        """
        if get_widget is None:
            get_widget = self.stack_layout.currentWidget()
        for name, widget in self.pages.items():
            if widget == get_widget:
                return name