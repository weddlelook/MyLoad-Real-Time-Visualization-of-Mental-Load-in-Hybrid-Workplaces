from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PyQt6.QtCore import QUrl, QTimer
import os

class JitsiWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.html_path = "app/view/styles/jitsi.html"
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        self.setLayout(layout)

    # takes the room_name from controller object in jitsi_page, and makes the browser show the intended html file.     
    def load_jitsi_meeting(self, room_name):
        self.browser.setUrl(QUrl(f"https://meet.jit.si/{room_name}"))  # Hier Meetinglink einfügen
        self.browser.setHtml(self.html_content)

    # takes the html file from html_path and replaces the room_name variable with the from user inputed room name
    def get_html_content(self, room_name): 
        try:
            with open(self.html_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            # Room name change
            html_content = html_content.replace("{{ room_name }}", room_name)
            return html_content
        except FileNotFoundError:
            print(f"Error: {file_path} didn't found")
            return "<h1>File wasn't found</h1>"