from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QSpacerItem, \
    QSizePolicy, QMessageBox, QDialog, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl, QTimer, Qt, pyqtSignal
import os
from pathlib import Path
#from .widget_Plot import EEGPlotWidget
from .widget_indicator import Indicator
from ..constants import *


class CustomWebEnginePage(QWebEnginePage):
    """ Custom WebEnginePage to handle permissions (audio/mic) """

    def __init__(self, parent=None):
        super().__init__(parent)
        ''' on permission request connects onFeaturePermissionRequested-method'''
        self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)

    def onFeaturePermissionRequested(self, securityOrigin, feature):
        """ Automatically grant microphone and video permissions """
        if feature in [
            QWebEnginePage.Feature.MediaAudioCapture,
            QWebEnginePage.Feature.MediaVideoCapture,
            QWebEnginePage.Feature.MediaAudioVideoCapture
        ]:
            self.setFeaturePermission(securityOrigin, feature, QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)


class ExitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Exit Confirmation")
        self.setFixedSize(400, 150)
        layout = QVBoxLayout()
        question = QLabel("Are you sure you want to exit?")
        question.setObjectName("text")
        layout.addWidget(question, alignment=Qt.AlignmentFlag.AlignCenter)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.close)

        h_layout = QHBoxLayout()

        h_layout.addWidget(self.back_button)
        h_layout.addWidget(self.exit_button)

        layout.addLayout(h_layout)

        self.setLayout(layout)


class JitsiWidget(QWidget):

    commentSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.plot_widget = Indicator()
        self.dialog = ExitDialog(self)
        self.initUI()
        self.set_settings()
        self.comment1 = None

    def initUI(self):
        #Layouts
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        #Jitsi Browser
        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebEnginePage(self.browser))

        #End Meeting Button
        self.end_button = QPushButton("End Meeting")
        #User Input for Notes/Highlights
        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Comment...")
        self.comment_sent_button = QPushButton("Comment Sent")

        # Comment confirmation message
        self.message_label = QLabel()
        self.message_label.setObjectName("text")
        self.message_label.setWordWrap(True)
        # Timer for message
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_message)

        left_layout.addWidget(self.browser)
        right_widget = self.plot_widget

        right_layout.addWidget(right_widget)
        right_layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignBottom)
        right_layout.addWidget(self.comment_input, alignment=Qt.AlignmentFlag.AlignBottom)
        right_layout.addWidget(self.comment_sent_button, alignment=Qt.AlignmentFlag.AlignBottom)

        spacer = QSpacerItem(20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        right_layout.addItem(spacer)

        right_layout.addWidget(self.end_button, alignment=Qt.AlignmentFlag.AlignBottom)

        self.end_button.clicked.connect(self.dialog.exec)

        main_layout.addLayout(left_layout, 9)  # 90% of the space
        main_layout.addLayout(right_layout, 1)  # 10% of the space

        self.setLayout(main_layout)
        self.comment_sent_button.clicked.connect(self.emit_user_input)

    def set_settings(self):
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)

    ''' takes the room_name from controller object in jitsi_page, and makes the browser show the intended html file. '''
    def load_jitsi_meeting(self, room_name):
        html_path = getAbsPath(FILE_PATH_JITSI_HTML)

        url = QUrl.fromLocalFile(str(html_path))
        url.setQuery(f"room_name={room_name}")

        self.browser.setUrl(url)

    def end_meeting(self):
        """ Calls JavaScript function to end the meeting """
        self.browser.page().runJavaScript("endMeeting();")  # ✅ Call the JS function

    def hide_ClScore(self):
        self.plot_widget.hide()

    def show_ClScore(self):
        self.plot_widget.show()

    def clear_message(self):
        # Clear the message label
        self.message_label.clear()
        self.timer.stop()

    def show_message(self, message):
        self.message_label.setText(message)
        # Start the timer to clear the message after 1 seconds
        self.timer.start(1000)  # 1000 ms = 1 seconds

    def emit_user_input(self):
        self.comment = self.comment_input.text().strip()
        if self.comment:
            self.commentSignal.emit(self.comment)
            self.show_message("Comment successfully sent!")
        self.comment_input.clear()


