from PySide6.QtCore import QObject, QThread, Qt, Signal, Slot
from PySide6.QtGui import QFontDatabase, QTextCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from meowgotchi.config import OLLAMA_MODEL, SYSTEM_PROMPT
from meowgotchi.ollama_client import chat
from meowgotchi.paths import FONT_PATH
from meowgotchi.ui_helpers import make_btn


class OllamaWorker(QObject):
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, messages):
        super().__init__()
        self.messages = messages

    @Slot()
    def run(self):
        message, error = chat(self.messages)
        if error is not None:
            self.failed.emit(error)
            return

        self.finished.emit(message)


class ChatPage(QWidget):
    def __init__(self, on_to_pet=None):
        super().__init__()
        self.on_to_pet = on_to_pet
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]
        self.thread = None
        self.worker = None

        font = QFontDatabase.addApplicationFont(str(FONT_PATH))
        PIXEL_FONT = QFontDatabase.applicationFontFamilies(font)[0]

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(360, 430)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel(f"Pet Chat Model: {OLLAMA_MODEL}")
        title.setStyleSheet(f"font-family: '{PIXEL_FONT}'; font-size: 16px; color: #ad4785;")

        back_btn = make_btn(
            "Pet",
            "transparent",
            "#ad4785",
            self.go_back,
            PIXEL_FONT
        )
        header.addWidget(title)
        header.addStretch()
        header.addWidget(back_btn)
        layout.addLayout(header)

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setPlainText("Meowgotchi: Hi i'm your pet but ask me anything.\n")
        self.chat_box.setStyleSheet(f"""
            QTextEdit {{
                background-color: #f7e4aa;
                color: #2b2230;
                border: 3px solid #ad4785;
                border-radius: 8px;
                padding: 8px;
                font-family: '{PIXEL_FONT}';
                font-size: 13px;
            }}
        """)
        layout.addWidget(self.chat_box)

        input_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Message ur pet...")
        self.input.returnPressed.connect(self.send_message)
        self.input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #eec7bd;
                color: #2b2230;
                border: 3px solid #ad4785;
                border-radius: 8px;
                padding: 8px;
                font-family: '{PIXEL_FONT}';
                font-size: 13px;
            }}
        """)

        self.send_btn = make_btn(
            "Pet",
            "transparent",
            "#ad4785",
            self.go_back,
            PIXEL_FONT
        )

        self.send_btn = make_btn(
            "Send",
            "#ad4785",
            "#ffffff",
            self.send_message,
            PIXEL_FONT
        )



        input_row.addWidget(self.input)
        input_row.addWidget(self.send_btn)
        layout.addLayout(input_row)
        self.setLayout(layout)


    def append_chat(self, speaker, text):
        self.chat_box.append(f"{speaker}: {text}")

    def send_message(self):
        text = self.input.text().strip()
        if not text or self.thread is not None:
            return

        self.input.clear()
        self.append_chat("You", text)
        self.append_chat("Meowgotchi", "thinking...")
        self.messages.append({"role": "user", "content": text})
        self.set_waiting(True)

        self.thread = QThread()
        self.worker = OllamaWorker(self.messages.copy())
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_reply)
        self.worker.failed.connect(self.on_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.clear_worker)
        self.thread.start()

    def set_waiting(self, waiting):
        self.input.setDisabled(waiting)
        self.send_btn.setDisabled(waiting)

    def on_reply(self, reply):
        self.remove_thinking_line()
        self.append_chat("Meowgotchi", reply)
        self.messages.append({"role": "assistant", "content": reply})
        self.set_waiting(False)

    def on_error(self, error):
        self.remove_thinking_line()
        self.append_chat("Meowgotchi", error)
        self.set_waiting(False)

    def remove_thinking_line(self):
        text = self.chat_box.toPlainText()
        self.chat_box.setPlainText(text.replace("\nMeowgotchi: i'm twinking really hard", "", 1))
        self.chat_box.moveCursor(QTextCursor.MoveOperation.End)

    def clear_worker(self):
        self.thread = None
        self.worker = None

    def go_back(self):
        if self.on_to_pet is not None:
            self.on_to_pet()

    def mousePressEvent(self, event):
        self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_start_position)

