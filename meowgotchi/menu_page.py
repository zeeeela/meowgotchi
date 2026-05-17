from PySide6.QtCore import  Qt
from PySide6.QtGui import QFontDatabase, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
)
from meowgotchi.paths import FONT_PATH, LAYOUT_ICON_PATH, PLAY_ICON_PATH, STOP_ICON_PATH, NEXT_ICON_PATH, PREV_ICON_PATH
from meowgotchi.ui_helpers import make_btn
import subprocess
import time

class MenuPage(QWidget):
    def __init__(self, on_to_song=None):
        super().__init__()
        self.on_to_song = on_to_song
        self.spotify_process = None

        font = QFontDatabase.addApplicationFont(str(FONT_PATH))
        PIXEL_FONT = QFontDatabase.applicationFontFamilies(font)[0]

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
        self.setFixedSize(360, 430)

        self.image = QLabel(self)
        self.image.setGeometry(0, 0, 332, 402)
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setPixmap(
            QPixmap(str(LAYOUT_ICON_PATH)).scaled(
                self.image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

        song_callback = on_to_song if on_to_song is not None else self.start_spotify_player

        title = QLabel("Dudu's Meowsic Pick", self)
        title.setStyleSheet(f"font-family: '{PIXEL_FONT}'; font-size: 16px;")
        title.setGeometry(0, 82, 320, 30) 
        title.setAlignment(Qt.AlignCenter)

        self.song_btn = make_btn(
            "",
            "transparent",
            "",
            song_callback,
            PIXEL_FONT,
            str(PLAY_ICON_PATH),
        )
        self.song_btn.setParent(self)
        self.song_btn.setFixedWidth(90)
        
        
        self.stop_btn = make_btn(
            "",
            "transparent",
            "",
            self.kill_spotify_player,
            PIXEL_FONT,
            str(STOP_ICON_PATH),
        ) 
        self.stop_btn.setParent(self)
        self.stop_btn.setFixedWidth(60)

        self.next_btn = make_btn(
            "",
            "transparent",
            "",
            self.next_track,
            PIXEL_FONT,
            str(NEXT_ICON_PATH),
        )
        self.next_btn.setParent(self)
        self.next_btn.setFixedWidth(80)
        self.next_btn.raise_()


        self.prev_btn = make_btn(
            "",
            "transparent",
            "",
            self.prev_track,
            PIXEL_FONT,
            str(PREV_ICON_PATH),
        )
        self.prev_btn.setParent(self)
        self.prev_btn.setFixedWidth(80)
        self.prev_btn.raise_()

        button_spacing = 10
        button_y = 185
        group_width = self.prev_btn.width() + self.song_btn.width() + self.next_btn.width() + button_spacing * 2
        start_x = (self.image.width() - group_width) // 2

        self.prev_btn.move(start_x + 6, button_y)
        self.song_btn.move(start_x + self.prev_btn.width() + button_spacing, button_y)
        self.next_btn.move(start_x + self.prev_btn.width() + self.song_btn.width() + button_spacing * 2 - 6, button_y)

        self.stop_btn.move(self.image.width() - self.stop_btn.width() - 16, 79)
        self.song_btn.raise_()
        self.stop_btn.raise_()

    def on_chat_click(self):
        print("Chat button clicked!")

    def on_song_click(self):
        print("Meowsic button clicked!")

    def start_spotify(self):
        try:
            subprocess.Popen(["open", "-a", "Spotify"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Spotify opened.")
        except FileNotFoundError:
            print("Spotify not found. Please open it manually.")
    
    def start_spotify_player(self):
        playlist_id = "08vvZBc99rdKTYlZhA7DYv"
        try:
            # Start the spotify_player in background
            self.spotify_process = subprocess.Popen(
                ["spotify_player"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
            # Give it time to start
            time.sleep(6)
        
            # Play using context command
            subprocess.run(
                ["spotify_player", "playback", "start", "context", "playlist", "--id", playlist_id],
                timeout=5
            )
            print(f"Playing playlist: {playlist_id}")
        
        except subprocess.TimeoutExpired:
            print("Command timed out")
        except FileNotFoundError:
            print("Spotify_player not found")
        except Exception as e:
            print(f"Error: {e}")

    def start_spotify_liked_songs(self):
        try:
            # First ensure spotify_player is running
            self.spotify_process = subprocess.Popen(
                ["spotify_player"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
            # Give it a moment to start
            time.sleep(2)
        
            # Play liked songs
            subprocess.run(
                ["spotify_player", "playback", "start", "liked"],
                timeout=5
            )
            print("Playing liked songs")
        except subprocess.TimeoutExpired:
            print("Command timed out")
        except FileNotFoundError:
            print("Spotify_player not found")
        except Exception as e:
            print(f"Error: {e}")

    def next_track(self):
        try:
            subprocess.run(
                ["spotify_player", "playback", "next"],
                timeout=5
                )
            print("Playing next track")
        except subprocess.TimeoutExpired:
            print("Command timed out")
        except FileNotFoundError:
            print("Spotify_player not found")
        except Exception as e:
            print(f"Error: {e}")

    def prev_track(self):
        try:
            subprocess.run(
                ["spotify_player", "playback", "previous"],
                timeout=5
                )
            print("Playing previous track")
        except subprocess.TimeoutExpired:
            print("Command timed out")
        except FileNotFoundError:
            print("Spotify_player not found")
        except Exception as e:
            print(f"Error: {e}")

    def kill_spotify_player(self):
        self.hide()
        try:
            if self.spotify_process:
                self.spotify_process.terminate()
                try:
                    self.spotify_process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    self.spotify_process.kill()
            subprocess.run(["pkill", "-9", "spotify_player"], check=False)
            print("Spotify player stopped.")
        except Exception as e:
            print(f"Error stopping Spotify playrer: {e}")

    def mousePressEvent(self, event):
        self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_start_position)