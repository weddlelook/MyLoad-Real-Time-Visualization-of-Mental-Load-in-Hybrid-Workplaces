from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton, QMessageBox, QStyle
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap
import Ressources as ressources
from click import style
from setuptools.warnings import InformationOnly


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
        layout.addWidget(self.startMaxtestButton, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)  # Button ausrichten und einfügen



        # Button zum skippen des Maxtests
        self.skipMaxtestButton = QPushButton("Skip")
        layout.addWidget(self.skipMaxtestButton, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter) # Button ausrichten und einfügen



        # Popup als Info zum skippen / Kann man sich überlegen das direkt auf den skip button zu machen
        self.infoButton = QPushButton("")
        self.info_icon = QLabel()
        self.pixmap = QPixmap()
        self.info_icon.setPixmap(self.pixmap)
        layout.addWidget(self.info_icon, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)



        self.infoButton.setToolTip("Diese Funktion macht nur Sinn falls Sie schon eine gespeicherte Sesssion haben bei denen Ihre umstände ca gleich sind, wie z.B schlaf, Uhrzeit, keine großen Änderungen in Ihrem Leben etc.")
        layout.addWidget(self.infoButton, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)



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
        self.infoButton.setFixedSize(button_width, button_height)