from PyQt6.QtWidgets import QStackedLayout, QMainWindow, QVBoxLayout, QWidget, QToolBar, QLineEdit
from PyQt6.QtGui import QFontDatabase, QFont, QAction, QIcon
from app.view.mainWidget import MainWidget
import os

class RootWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()

        self.setWindowTitle("MyLoad")
        self.settings = settings
        #Set minimum size for application window
        self.setMinimumSize(733, 550)
        self.main_window = MainWidget()
        self.setCentralWidget(self.main_window)
        self.apply_font()
        self.create_toolbar()
        self.apply_stylesheet()
        self.show()

    def apply_stylesheet(self):
        if self.settings["lightMode"] == 1:
            file_path = r"app/view/styles/style_light.qss"
        elif self.settings["darkMode"] == 1:
            file_path = r"app/view/styles/style_dark.qss"
        try:
            with open(file_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: Stylesheet '{file_path}' not found.")

    def create_toolbar(self):
        toolbar = self.addToolBar('Main Toolbar')
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.settings_action = QAction(QIcon("app/view/styles/images/settings-icon.png"), 'Settings', self)
        self.retrospective_action = QAction("Previous Sessions", self)
        toolbar.addAction(self.settings_action)
        toolbar.addAction(self.retrospective_action)

    def show_toolbar(self, show):
        if show:
            self.findChild(QToolBar).setVisible(True)
        elif not show:
            self.findChild(QToolBar).setVisible(False)

    @staticmethod
    def apply_font():
        font_path = os.path.join(os.path.dirname(__file__), r"styles/fonts/Lexend-VariableFont_wght.ttf")
        print(font_path)
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                # Retrieve the family name of the loaded font
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    print(f"✅ Font loaded successfully: {families[0]}")
                else:
                    print("⚠ ERROR: No font families were found.")

