from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFontDatabase
from meowgotchi.paths import FONT_PATH, MENU_ICON_PATH, STOP_ICON_PATH, github_activity_image_path
from meowgotchi.heatmap_streak import generate_github_activity_heatmap
from meowgotchi.ui_helpers import make_btn

class ActivityPage(QWidget):
    def __init__(self, on_to_menu=None):
        super().__init__()

        font = QFontDatabase.addApplicationFont(str(FONT_PATH))
        PIXEL_FONT = QFontDatabase.applicationFontFamilies(font)[0]

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)

        self.stop_btn = make_btn(
            "",
            "transparent",
            "",
            self.hide_page,
            PIXEL_FONT,
            str(STOP_ICON_PATH),
        ) 

        layout.addWidget(self.stop_btn, alignment=Qt.AlignRight)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.refresh_activity_image()

    def refresh_activity_image(self):
        image_path = github_activity_image_path()
        if not image_path.exists():
            generate_github_activity_heatmap(image_path=image_path)

        self.image = QPixmap(str(image_path))
        self.image = self.image.scaled(560.7, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(self.image)

    def showEvent(self, event):
        self.refresh_activity_image()
        super().showEvent(event)

    def hide_page(self):
        self.hide()

    def mousePressEvent(self, event):
        self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_start_position)



