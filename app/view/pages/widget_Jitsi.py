from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QSpacerItem, \
    QSizePolicy, QMessageBox, QDialog, QLabel, QApplication, QToolTip
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl, QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
import os
from pathlib import Path
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


class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Create a signal for the click event

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # Make it look clickable

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


class JitsiWidget(QWidget):

    commentSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.plot_widget = Indicator()
        self.dialog = ExitDialog(self)
        self.initUI()
        self.set_settings()
        self.comment = None

    def initUI(self):
        #Layouts
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        #Jitsi Browser

        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebEnginePage(self.browser))
        left_layout.addWidget(self.browser)



        # Plot Icon
        self.plot_icon = ClickableLabel(self)
        self.open_eye_icon = QPixmap(getAbsPath(FILE_PATH_OPEN_EYE_ICON)).scaled(32, 32,
                                                                                 Qt.AspectRatioMode.KeepAspectRatio,
                                                                                 Qt.TransformationMode.SmoothTransformation)
        self.closed_eye_icon = QPixmap(getAbsPath(FILE_PATH_CLOSED_EYE_ICON)).scaled(32, 32,
                                                                                     Qt.AspectRatioMode.KeepAspectRatio,
                                                                                     Qt.TransformationMode.SmoothTransformation)

        self.plot_icon.setPixmap(self.open_eye_icon)
        self.plot_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plot_icon.setToolTip("Click to hide your cognitive load score")
        self.plot_icon.clicked.connect(self.toggle_button)
        self.plot_icon.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.plot_height = self.plot_widget.height()

        #Info Icon
        self.info_icon = QLabel(self)
        path_info_icon = getAbsPath(FILE_PATH_INFO_ICON)
        self.info_icon.setPixmap(QPixmap(path_info_icon).scaled(26, 26, Qt.AspectRatioMode.KeepAspectRatio,
                                                                Qt.TransformationMode.SmoothTransformation))
        self.info_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.info_icon.setToolTip("The score displayed represents your Cognitive Load (CL) score."
                                  " It is calculated using various values recorded by the headphones"
                                  " and processed through a formula to standardize it, allowing for"
                                  " comparison with your previous sessions.")  # Tooltip for new icon
        self.info_icon.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Spacer to fill the gap between plot widget and rest of the widgets
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Comment confirmation message
        self.message_label = QLabel()
        self.message_label.setObjectName("text")
        self.message_label.setWordWrap(True)
        # Timer for message
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_message)


        #User Input for Notes/Highlights
        self.comment_input = QLineEdit()
        self.comment_sent_button = QPushButton("Comment Sent")
        self.comment_input.setPlaceholderText("Comment...")
        self.comment_sent_button.clicked.connect(self.emit_user_input)

        #Break Button
        self.break_button = QPushButton("Pause")
        self.break_button.setToolTip("Click to  pause or resume the recording")
        self.break_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.break_button.clicked.connect(self.manage_break)

        #End Meeting Button
        self.end_button = QPushButton("End Meeting")
        self.end_button.clicked.connect(self.dialog.exec)

        right_layout.addWidget(self.plot_icon, alignment=Qt.AlignmentFlag.AlignTop)
        right_layout.addWidget(self.info_icon, alignment=Qt.AlignmentFlag.AlignTop)
        right_layout.addWidget(self.plot_widget)
        right_layout.addItem(spacer)
        right_layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignBottom)
        right_layout.addWidget(self.comment_input, alignment=Qt.AlignmentFlag.AlignBottom)
        right_layout.addWidget(self.comment_sent_button, alignment=Qt.AlignmentFlag.AlignBottom)
        right_layout.addWidget(self.break_button, alignment=Qt.AlignmentFlag.AlignBottom)
        right_layout.addWidget(self.end_button, alignment=Qt.AlignmentFlag.AlignBottom)

        main_layout.addLayout(left_layout, 90)  # 90% of the space
        main_layout.addLayout(right_layout, 10)  # 10% of the space

        self.setLayout(main_layout)

    ''' takes the room_name from controller object in jitsi_page, and makes the browser show the intended html file. '''
    def load_jitsi_meeting(self, room_name, user_name):
        html_path = getAbsPath(FILE_PATH_JITSI_HTML)

        url = QUrl.fromLocalFile(str(html_path))
        url.setQuery(f"room_name={room_name}")
        self.browser.setUrl(url)

        self.show_ClScore()
        self.plot_icon.setPixmap(self.open_eye_icon)
        self.plot_icon.setToolTip("Click to hide your cognitive load score")

        if user_name:
            QTimer.singleShot(2000, lambda: self.browser.page().runJavaScript(f'setDisplayName(\"{user_name}\")'))

    def end_meeting(self):
        """ Calls JavaScript function to end the meeting """
        self.browser.page().runJavaScript("endMeeting();")  # ✅ Call the JS function

    def hide_ClScore(self):
        self.plot_widget.setFixedHeight(0)

    def show_ClScore(self):
        self.plot_widget.setFixedHeight(self.plot_height)

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

    def toggle_button(self):
        if self.plot_widget.height() > 0:
            self.hide_ClScore()
            self.plot_icon.setPixmap(self.closed_eye_icon)
            self.plot_icon.setToolTip("Click to show your cognitive load score")
        else:
            self.show_ClScore()
            self.plot_icon.setPixmap(self.open_eye_icon)
            self.plot_icon.setToolTip("Click to hide your cognitive load score")

    # TODO: write the method to manage breaks (Pause/Resume)
    def manage_break(self):
        if self.break_button.text() == "Pause":
            self.break_button.setText("Resume")
            pass
        else:
            self.break_button.setText("Pause")
            pass

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

