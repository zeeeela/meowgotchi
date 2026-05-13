from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter


def make_btn(text, bg, fg, slot, PIXEL_FONT, icon1=None, icon2=None):
    btn = QPushButton(text)
    icon_size = QSize(30, 30)

    def keep_ratio_icon(path):
        source = QPixmap(path)
        scaled = source.scaled(
            icon_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        canvas = QPixmap(icon_size)
        canvas.fill(Qt.GlobalColor.transparent)

        painter = QPainter(canvas)
        x = (icon_size.width() - scaled.width()) // 2
        y = (icon_size.height() - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)
        painter.end()

        return QIcon(canvas)

    if icon1 is not None:
        btn.setIcon(keep_ratio_icon(icon1))
        btn.setIconSize(icon_size)
        if icon2 is not None:
            btn.pressed.connect(lambda: btn.setIcon(keep_ratio_icon(icon2)))
            btn.released.connect(lambda: btn.setIcon(keep_ratio_icon(icon1)))

    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setFixedHeight(40 if icon1 is not None else 10)
    align_style = "text-align: left;" if icon1 is not None else ""
    btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {bg};
            color: {fg};
            font-size: 12px;
            font-weight: bold;
            border-radius: 8px;
            padding: 0 10px;
            font-family: '{PIXEL_FONT}';
            {align_style}
        }}
        QPushButton:hover   {{ opacity: 0.85; }}
        QPushButton:pressed {{ background-color: {fg}; color: {bg}; }}
    """)
    btn.clicked.connect(slot)
    return btn
