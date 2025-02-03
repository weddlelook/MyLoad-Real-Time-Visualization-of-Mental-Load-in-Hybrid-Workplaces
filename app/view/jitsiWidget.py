from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl, QTimer, Qt
import os
from pathlib import Path
from app.view.plotWidget import EEGPlotWidget


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


class JitsiWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plot_widget = EEGPlotWidget()
        self.initUI()
        self.set_settings()

    def initUI(self):
        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebEnginePage(self.browser))

        self.end_button = QPushButton("End Meeting")

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.browser)
        left_layout.addWidget(self.end_button, alignment=Qt.AlignmentFlag.AlignCenter)
        right_widget = self.plot_widget

        main_layout.addLayout(left_layout)
        main_layout.addWidget(right_widget)

        self.setLayout(main_layout)

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
        base_path = Path(__file__).resolve().parent
        html_path = base_path / "styles" / "jitsi.html"

        url = QUrl.fromLocalFile(str(html_path))
        url.setQuery(f"room_name={room_name}")

        self.browser.setUrl(url)

    def end_meeting(self):
        """ Calls JavaScript function to end the meeting """
        self.browser.page().runJavaScript("endMeeting();")  # ✅ Call the JS function