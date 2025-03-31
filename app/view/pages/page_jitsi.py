from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSpacerItem,
    QSizePolicy,
    QDialog,
    QLabel,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtCore import QUrl, QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

from pathlib import Path
from .widget_indicator import Indicator
from ..constants import *


class JitsiPage(QWidget):
    """Main Widget handling Jitsi integration"""

    commentSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.plot_widget = Indicator()
        self.dialog = self.ExitDialog(self)

        self.comment = None
        self.plot_height = self.plot_widget.height()
        self.initUI()
        self._set_browser_settings()

    def initUI(self):
        """Initialize UI layout and widgets"""

        # Layouts
        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Browser widget setup
        self.browser = QWebEngineView()
        self.browser.setPage(self.CustomWebEnginePage(self.browser))
        left_layout.addWidget(self.browser)

        # Plot Icon
        self.plot_icon = self.ClickableLabel(self)
        self.plot_icon.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.open_eye_icon, self.closed_eye_icon = self._load_icons()
        self.toggle_plot_icon(is_open=True)
        self.plot_icon.clicked.connect(self.toggle_plot_widget)

        # Info Icon
        self.info_icon_cl = self._create_icon_label(
            FILE_PATH_INFO_ICON, tooltip=(JITSI_PAGE_INFO)
        )
        self.info_icon_cl.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Message label
        self.message_label = QLabel(objectName="text", wordWrap=True)

        # Timer to clear message after a certain time of no interaction
        self.message_timeout = QTimer()
        self.message_timeout.timeout.connect(self._clear_message)

        # Input & Buttons
        self.comment_input = QLineEdit(placeholderText="Comment...")
        self.comment_sent_button = self._create_button(
            "Comment Sent",
            self.emit_user_input,
            tooltip="Comment to leave a mark on graph",
        )
        self.break_button = self._create_button(
            "Pause", self.toggle_monitoring, tooltip="Click to pause the monitoring"
        )
        self.end_button = self._create_button("End Meeting", self.dialog.exec)

        # Right Layout Organization
        right_layout.addWidget(self.plot_icon, alignment=Qt.AlignmentFlag.AlignTop)
        right_layout.addWidget(self.info_icon_cl, alignment=Qt.AlignmentFlag.AlignTop)
        right_layout.addWidget(self.plot_widget)
        right_layout.addItem(
            QSpacerItem(
                20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
        )
        right_layout.addWidget(
            self.message_label, alignment=Qt.AlignmentFlag.AlignBottom
        )
        right_layout.addWidget(
            self.comment_input, alignment=Qt.AlignmentFlag.AlignBottom
        )
        right_layout.addWidget(
            self.comment_sent_button, alignment=Qt.AlignmentFlag.AlignBottom
        )
        right_layout.addWidget(
            self.break_button, alignment=Qt.AlignmentFlag.AlignBottom
        )
        right_layout.addWidget(self.end_button, alignment=Qt.AlignmentFlag.AlignBottom)

        # Main Layout Organization
        main_layout.addLayout(left_layout, 90)
        main_layout.addLayout(right_layout, 10)

    def toggle_monitoring(self):
        if self.break_button.text() == "Pause":
            self.break_button.setText("Resume")
            self.break_button.setToolTip("Click to resume the monitoring")
        else:
            self.break_button.setText("Pause")
            self.break_button.setToolTip("Click to pause the monitoring")

    def toggle_plot_icon(self, is_open):
        """Update plot icon state"""
        self.plot_icon.setPixmap(
            self.open_eye_icon if is_open else self.closed_eye_icon
        )
        self.plot_icon.setToolTip(
            "Click to hide your cognitive load score"
            if is_open
            else "Click to show your cognitive load score"
        )

    def toggle_plot_widget(self):
        """Toggle plot widget visibility"""
        is_visible = self.plot_widget.height() > 0
        self.plot_widget.setFixedHeight(0 if is_visible else self.plot_height)
        self.toggle_plot_icon(not is_visible)

    def emit_user_input(self):
        """Emit user input comment"""
        self.comment = self.comment_input.text().strip()
        if self.comment:
            self.commentSignal.emit(self.comment)
            if self.break_button.text() == "Pause":
                self._show_sent_message("Comment successfully sent!")
            else:
                self._show_sent_message("Comments on break won't be saved!")
        self.comment_input.clear()

    def end_meeting(self):
        """Calls JavaScript function to end the meeting"""
        self.browser.page().runJavaScript("endMeeting();")

    def load_jitsi_meeting(self, room_name, user_name):
        html_path = getAbsPath(FILE_PATH_JITSI_HTML)

        url = QUrl.fromLocalFile(str(html_path))
        url.setQuery(f"room_name={room_name}")
        self.browser.setUrl(url)

        self.plot_widget.setFixedHeight(self.plot_height)

        if user_name:
            QTimer.singleShot(
                2000,
                lambda: self.browser.page().runJavaScript(
                    f'setDisplayName("{user_name}")'
                ),
            )

    def _show_sent_message(self, message):
        """Show and clear message after delay"""
        self.message_label.setText(message)
        self.message_timeout.start(1000)

    def _clear_message(self):
        """Clear message label"""
        self.message_label.clear()
        self.message_timeout.stop()

    def _create_button(self, text, callback, tooltip=None):
        """Helper function to create a button"""
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        if tooltip:
            button.setToolTip(tooltip)
        return button

    def _create_icon_label(self, file_path, tooltip=None):
        """Helper function to create an icon label"""
        label = QLabel(self)
        label.setPixmap(
            QPixmap(getAbsPath(file_path)).scaled(
                26,
                26,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        label.setCursor(Qt.CursorShape.PointingHandCursor)
        if tooltip:
            label.setToolTip(tooltip)
        return label

    def _load_icons(self):
        """Load and return open/closed eye icons"""
        return (
            QPixmap(getAbsPath(FILE_PATH_OPEN_EYE_ICON)).scaled(
                32,
                32,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            ),
            QPixmap(getAbsPath(FILE_PATH_CLOSED_EYE_ICON)).scaled(
                32,
                32,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            ),
        )

    def _set_browser_settings(self):
        """Configure browser settings"""
        settings = self.browser.settings()
        for attr in [
            QWebEngineSettings.WebAttribute.JavascriptEnabled,
            QWebEngineSettings.WebAttribute.LocalStorageEnabled,
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
            QWebEngineSettings.WebAttribute.AllowRunningInsecureContent,
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls,
            QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript,
            QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins,
        ]:
            settings.setAttribute(attr, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)


    class CustomWebEnginePage(QWebEnginePage):
        """Custom WebEnginePage to handle permissions (audio/mic)"""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)

        def onFeaturePermissionRequested(self, securityOrigin, feature):
            """Automatically grant microphone and video permissions"""
            if feature in {
                QWebEnginePage.Feature.MediaAudioCapture,
                QWebEnginePage.Feature.MediaVideoCapture,
                QWebEnginePage.Feature.MediaAudioVideoCapture,
            }:
                self.setFeaturePermission(
                    securityOrigin,
                    feature,
                    QWebEnginePage.PermissionPolicy.PermissionGrantedByUser,
                )

    class ExitDialog(QDialog):
        """Exit confirmation dialog"""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Exit Confirmation")
            self.setFixedSize(400, 150)
            layout = QVBoxLayout(self)

            question = QLabel("Are you sure you want to exit?", objectName="text")
            layout.addWidget(question, alignment=Qt.AlignmentFlag.AlignCenter)

            button_layout = QHBoxLayout()
            self.exit_button = self.create_button("Exit", self.close)
            self.back_button = self.create_button("Back", self.close)

            button_layout.addWidget(self.back_button)
            button_layout.addWidget(self.exit_button)
            layout.addLayout(button_layout)

        def create_button(self, text, callback):
            """Helper function to create a button with a callback"""
            button = QPushButton(text)
            button.clicked.connect(callback)
            return button

    class ClickableLabel(QLabel):
        """Custom QLabel that emits a signal when clicked"""

        clicked = pyqtSignal()

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setCursor(Qt.CursorShape.PointingHandCursor)

        def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.clicked.emit()
