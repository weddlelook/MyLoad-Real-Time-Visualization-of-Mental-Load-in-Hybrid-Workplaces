from PyQt6.QtWidgets import (
    QStackedLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QLineEdit,
    QMessageBox,
)
from PyQt6.QtGui import QFontDatabase, QFont, QAction, QIcon
from .mainWidget import MainWidget
from .constants import *
import os


class RootWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()

        self.setWindowTitle("MyLoad")
        self.setting = settings
        self.apply_stylesheet(settings)

        # Set minimum size for application window
        self.setMinimumSize(733, 733)
        # Set default window size
        self.resize(1200, 733)

        self.main_window = MainWidget()
        self.main_window.settings.new_settings.connect(self.apply_stylesheet)
        self.main_window.settings.new_settings.connect(self.main_window.toggle_settings)
        self.main_window.settings.back_button.clicked.connect(
            self.main_window.toggle_settings
        )
        self.setCentralWidget(self.main_window)
        self.apply_font()
        self.create_toolbar()
        self.show()
        self.settings_action.triggered.connect(self.main_window.toggle_settings)

        self.active_errors = (
            set()
        )  # Set to track active error messages, ensuring no duplicates

    def apply_stylesheet(self, settings):
        self.settings = settings
        if settings["isDarkMode"] == False:
            file_path = getAbsPath(FILE_PATH_CSS_LIGHTMODE)
        elif settings["isDarkMode"] == True:
            file_path = getAbsPath(FILE_PATH_CSS_DARKMODE)
        try:
            with open(file_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: Stylesheet '{file_path}' not found.")

    def create_toolbar(self):
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.settings_action = QAction(
            QIcon(getAbsPath(FILE_PATH_SETTINGS_ICON)), "Settings", self
        )
        self.retrospective_action = QAction("Previous Sessions", self)
        toolbar.addAction(self.settings_action)
        toolbar.addAction(self.retrospective_action)

    def show_toolbar(self, show):
        if show:
            self.findChild(QToolBar).setVisible(True)
        elif not show:
            self.findChild(QToolBar).setVisible(False)

    def display_error_message(self, message: str):
        """
        Displays an error message in a message box.
        :param message: The error message to display.
        """
        if message in self.active_errors:
            return  # Avoid showing the same error message multiple times

        self.active_errors.add(message)

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg_box.exec()

        self.active_errors.remove(message)

    @staticmethod
    def apply_font():
        if os.path.exists(getAbsPath(FILE_PATH_FONT)):
            font_id = QFontDatabase.addApplicationFont(getAbsPath(FILE_PATH_FONT))
            if font_id != -1:
                # Retrieve the family name of the loaded font
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    print(f"✅ Font loaded successfully: {families[0]}")
                else:
                    print("⚠ ERROR: No font families were found.")

    def closeEvent(self, event):
        """
        This method is automatically triggered when the user attempts to close the window.
        It displays a confirmation dialog asking if they really want to exit the application.
        - If the user selects "Yes", the window will close.
        - If the user selects "No", the closing action is canceled.
        This prevents accidental exits and allows the user to confirm their decision.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Close MyLoad")
        msg_box.setText("Are you sure you want to close MyLoad?")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.setIcon(QMessageBox.Icon.NoIcon)  # Entfernt das "i"-Symbol

        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
