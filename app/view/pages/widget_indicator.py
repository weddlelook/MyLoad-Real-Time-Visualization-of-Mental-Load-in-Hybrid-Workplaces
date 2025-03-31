from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt


class Indicator(QWidget):
    def __init__(self):
        super().__init__()
        self.value = 0  # initial value
        self.setMinimumSize(200, 150)

        self.label = QLabel(f"{self.value}", self)
        self.label.setObjectName("title")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_score(self, score):
        self.value = score
        self.label.setText(str(score))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        size = min(rect.width(), rect.height()) - 40
        center_x = rect.center().x()
        center_y = rect.top() + 40

        # empty circle (Gray)
        painter.setPen(
            QPen(QColor("#CCCCCC"), 15, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        )
        painter.drawArc(center_x - size // 2, center_y, size, size, 0 * 16, 180 * 16)

        # **full cycle** (blue, fills from left to right)
        filled_angle = int((self.value / 100) * 180)
        painter.setPen(
            QPen(QColor("#5FA9C0"), 15, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        )
        painter.drawArc(
            center_x - size // 2, center_y, size, size, 180 * 16, -filled_angle * 16
        )
        # place of the score label
        label_width = self.label.sizeHint().width()
        label_height = self.label.sizeHint().height()
        label_x = center_x - label_width // 2
        label_y = center_y + size // 2 - label_height // 2
        self.label.setGeometry(label_x, label_y, label_width, label_height)
