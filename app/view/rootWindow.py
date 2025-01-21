from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class RootWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.main_window = MainWidget()
        self.setCentralWidget(self.main_window)
        self.show()

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

    def add_child(self, child:QWidget):
        # clearLayout(self.layout)
        layout = QVBoxLayout()
        layout.addWidget(child)
        self.setLayout(layout)

