import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl


class CustomWebEnginePage(QWebEnginePage):
    """ Custom WebEnginePage to handle permissions (audio/mic) """
    
    def __init__(self, parent=None):
        super().__init__(parent)

    def acceptFeaturePermission(self, securityOrigin, feature, enable):
        """ Automatically grant microphone and audio permissions """
        if feature in [
            QWebEnginePage.Feature.MediaAudioCapture,
            QWebEnginePage.Feature.MediaVideoCapture,
            QWebEnginePage.Feature.MediaAudioVideoCapture
        ]:
            enable = True  # ✅ Allow access
        super().acceptFeaturePermission(securityOrigin, feature, enable)


class JitsiApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jitsi in PyQt6 - With API Controls")
        self.setGeometry(100, 100, 1280, 720)

        # Create layout and main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # WebEngineView for Jitsi
        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebEnginePage(self.browser))

        # Enable WebRTC, JavaScript, and audio permissions
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


        self.browser.setUrl(QUrl("file:///C:/Users/Clara/Desktop/MyLoad/tes_myload/references_and_loose_code_files/jitsi.html"))

        # Button to end the meeting
        self.end_button = QPushButton("")
        self.end_button.clicked.connect(self.end_meeting)

        # Add widgets to layout
        layout.addWidget(self.browser)
        layout.addWidget(self.end_button)

    def end_meeting(self):
        """ Calls JavaScript function to end the meeting """
        self.browser.page().runJavaScript("endMeeting();")  # ✅ Call the JS function


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JitsiApp()
    window.show()
    sys.exit(app.exec())
