import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flask ve PyQt6")

        # Flask server'ı başlat
        self.process = subprocess.Popen(["python", "app.py"])

        # QWebEngineView oluştur ve URL'yi ayarla
        self.browser = QWebEngineView()
        url = QUrl("http://127.0.0.1:5001/")  # QUrl nesnesi oluşturuluyor
        self.browser.setUrl(url)

        # Layout oluştur ve QWebEngineView ekle
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def closeEvent(self, event):
        # Uygulama kapanırken Flask server'ı durdur
        self.process.terminate()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())