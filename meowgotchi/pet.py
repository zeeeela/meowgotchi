from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap, QFontDatabase
from meowgotchi.paths import FONT_PATH, MENU_ICON_PATH, PET_IMAGE_PATH
from meowgotchi.ui_helpers import make_btn


class Pet(QWidget):
    def __init__(self, on_to_menu=None, on_to_research=None, on_to_chat=None, on_to_activity=None):
        super().__init__()

        font = QFontDatabase.addApplicationFont(str(FONT_PATH))
        PIXEL_FONT = QFontDatabase.applicationFontFamilies(font)[0]

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.image = QPixmap(str(PET_IMAGE_PATH))
        self.image = self.image.scaled(105, 105, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)

        self.image_label = QLabel()
        self.image_label.setPixmap(self.image)
        layout.addWidget(self.image_label)

        self.chat_btn = make_btn(
            "Chat",
            "transparent",
            "#ad4785",
            on_to_chat or self.on_button_click,
            PIXEL_FONT,
            str(MENU_ICON_PATH),
        )
        layout.addWidget(self.chat_btn)

        self.research_btn = make_btn(
            "Research",
            "transparent",
            "#ad4785",
            on_to_research or self.on_button_click,
            PIXEL_FONT,
            str(MENU_ICON_PATH),
        )
        layout.addWidget(self.research_btn)


        self.music_btn = make_btn(
            "Meowqsic",
            "transparent",
            "#ad4785",
            on_to_menu or self.on_button_click,
            PIXEL_FONT,
            str(MENU_ICON_PATH),
        )
        layout.addWidget(self.music_btn)

        self.github_btn = make_btn(
            "Github Activity",
            "transparent",
            "#ad4785",
            on_to_activity or self.on_button_click,
            PIXEL_FONT,
            str(MENU_ICON_PATH),
        )
        layout.addWidget(self.github_btn)

        self.setLayout(layout)

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

    # Placeholder to check if the button click is working.
    def on_button_click(self):
        print("Meow! The pet was clicked.")

