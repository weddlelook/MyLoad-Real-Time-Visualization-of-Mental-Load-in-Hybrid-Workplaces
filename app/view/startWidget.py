from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QLineEdit, \
    QGroupBox, QFormLayout

from PyQt6.QtCore import Qt, pyqtSignal
import sys

class StartWidget(QWidget):
    user_input_entered = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.session_name = None
        self.jitsi_room_name = None

    def initUI(self):
        self.setWindowTitle('Start Widget')
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(30, 20, 30, 20)

        #Title
        title_label = QLabel("Welcome to MyLoad")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        #Explanation
        text_label = QLabel(
            "MyLoad provide users the opportunity to monitor their cognitive load during online lectures,"
            " helping them optimize focus, productivity, and overall performance."
        )
        text_label.setObjectName("text")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)
        layout.addWidget(text_label)

        #Form layout for user inputs
        form_layout = QFormLayout()

        #Ask for session name
        self.label_session = QLabel("Please enter a label to identify following session.")
        self.label_session.setObjectName("subtitle")
        self.session_input = QLineEdit()
        self.session_input.setPlaceholderText('Session Name...')

        form_layout.addRow(self.label_session)
        form_layout.addRow(self.session_input)
        form_layout.setAlignment(self.label_session, Qt.AlignmentFlag.AlignCenter)
        form_layout.setAlignment(self.session_input, Qt.AlignmentFlag.AlignCenter)

        # Ask for jitsi meeting room name
        self.label_jitsi = QLabel("Please enter the name of Jitsi-Meeting room")
        self.label_jitsi.setObjectName("subtitle")
        self.jitsi_input = QLineEdit()
        self.jitsi_input.setPlaceholderText('Room Name...')

        form_layout.addRow(self.label_jitsi)
        form_layout.addRow(self.jitsi_input)
        form_layout.setAlignment(self.label_jitsi, Qt.AlignmentFlag.AlignCenter)
        form_layout.setAlignment(self.jitsi_input, Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(form_layout)

        #Start session button
        self.start_session_button = QPushButton('▶ Start a Session')
        layout.addWidget(self.start_session_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        #Assign a minimum size for the window
        self.setMinimumSize(600, 450)
        self.start_session_button.clicked.connect(self._emit_user_input)

    def _emit_user_input(self):
        self.session_name = self.session_input.text().strip()
        self.jitsi_room_name = self.jitsi_input.text().strip()
        if not self.session_name:
            self.label_session.setText("Please provide a label to proceed")
        if not self.jitsi_room_name:
            self.label_jitsi.setText("Please provide a room name to proceed")
        if self.session_name and self.jitsi_room_name:
            user_input = [self.session_name, self.jitsi_room_name]
            self.user_input_entered.emit(user_input)


