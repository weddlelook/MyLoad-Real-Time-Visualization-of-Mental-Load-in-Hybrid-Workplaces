from PyQt6.QtWidgets import QStackedLayout, QVBoxLayout, QWidget, QSizePolicy, QPushButton, QLabel, \
    QLineEdit

# Custom pages import
import app.view.pages as p

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
        self.main_layout.setContentsMargins(20, 10, 20, 10) #left top right bottom
        self.setLayout(self.main_layout)

        # Setting up Settings
        self.settings = p.SettingsWidget()

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
        self.settings.hide()

    def register_page(self, child: QWidget, page_name: str):
        """Registers a page with the main window."""
        self._apply_resize_policy(child)
        self.stack_layout.addWidget(child)
        self.pages[page_name] = child

    def _apply_resize_policy(self, widget: QWidget):
        """Recursively applies the size policy to all widgets in the page."""
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        for child in widget.findChildren(QWidget):
            child.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            if isinstance(child, QPushButton):
                child.setMinimumSize(100, 50)
            elif isinstance(child, QLabel):
                if child.objectName() == "title":
                    child.setMaximumHeight(250)
                elif child.objectName() == "text":
                    child.setMaximumHeight(200)
                elif child.objectName() == "subtitle":
                    child.setMaximumHeight(200)
                child.setMinimumSize(100, 30)
            elif isinstance(child, QLineEdit):
                child.setMinimumSize(120, 30)

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
            widget.load_sessions()
            widget.back_button.clicked.connect(lambda: self.set_page("start"))
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