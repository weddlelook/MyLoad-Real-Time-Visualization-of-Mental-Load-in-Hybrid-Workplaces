from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton, QMessageBox, QStyle
from PyQt6.QtCore import Qt, QSize, QDir
from PyQt6.QtGui import QFont, QIcon, QPixmap
from click import style
from setuptools.warnings import InformationOnly
import os


class StartMaxTestPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()



    def initUI(self):
        layout = QGridLayout()

        self.label = QLabel()
        self.label.setText("Jetzt testen wir noch Ihre Maximalauslastung!")

        # Text größer machen
        font = QFont("Arial", 20)  # Schriftart und Schriftgröße
        self.label.setFont(font)
        # Text ausrichten und einfügen
        layout.addWidget(self.label, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.ready = QLabel()
        self.ready.setText("Bereit?")


        # Text größer machen
        ready_font = QFont("Arial", 15)  # Schriftart und Schriftgröße
        self.label.setFont(ready_font)
        # Text ausrichten und einfügen
        layout.addWidget(self.ready, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)


        #Button zum starten des Maxtests
        self.startMaxtestButton = QPushButton("Start")
        layout.addWidget(self.startMaxtestButton, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter)  # Button ausrichten und einfügen



        # Button zum skippen des Maxtests
        self.skipMaxtestButton = QPushButton("Skip")
        layout.addWidget(self.skipMaxtestButton, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen



        # Popup als Info zum skippen / Kann man sich überlegen das direkt auf den skip button zu machen
        # Hier Icon einfügen
        self.info_icon = QLabel()
        bild_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Ressources/Information.png"))
        self.pixmap = QPixmap(bild_pfad) # geht aber wahrscheinlich net schön
        self.scaled_pixmap = self.pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
        self.info_icon.setPixmap(self.scaled_pixmap)
        layout.addWidget(self.info_icon, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.info_icon.setToolTip("Diese Funktion macht nur Sinn falls Sie schon eine gespeicherte Sesssion haben bei denen Ihre umstände ca gleich sind, wie z.B schlaf, Uhrzeit, keine großen Änderungen in Ihrem Leben etc.")






        self.setLayout(layout)
        self.setWindowTitle('StartMaxtest Widget')



    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Calculate 10% width and 15% height of the parent widget
        button_width = int(self.width() * 0.1)
        button_height = int(self.height() * 0.15)

        # Set button sizes dynamically
        self.startMaxtestButton.setFixedSize(button_width, button_height)
        self.skipMaxtestButton.setFixedSize(button_width, button_height)