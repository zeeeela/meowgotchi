from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap

class Pet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.image = QPixmap("black_meow.png")
        self.image = self.image.scaled(105, 105, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.resize(self.image.width(), self.image.height() + 30)  # Add space for button

        self.button = QPushButton("Feed Me")
        self.button.setGeometry(0, self.image.height(), self.image.width(), 30)
        self.button.clicked.connect(self.on_button_click)

    def mousePressEvent(self, event):
        self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_start_position)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image)

    def enterEvent(self, event):
        self.show()

    def on_button_click(self):
        print("Meow! The pet was clicked.")
