import subprocess
import sys
import atexit

from PySide6.QtWidgets import QApplication, QStyleFactory

from meowgotchi.chat_page import ChatPage
from meowgotchi.pet import Pet

def start_ollama():
    try:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Ollama server started.")
    except FileNotFoundError:
        print("Ollama not found. Please install it or run 'ollama serve' manually.")
        sys.exit(1)

def cleanup_ollama():
    """Kill Ollama when app exits"""
    try:
        subprocess.run(["pkill", "-f", "ollama"], check=False)
        print("Ollama server stopped.")
    except FileNotFoundError:
        pass

class AppController:
    def __init__(self):
        self.pet = Pet(on_to_menu=self.show_menu)
        self.menu = ChatPage(on_to_pet=self.show_pet)

    def show_pet(self):
        cleanup_ollama()
        self.menu.hide()
        self.pet.show()

    def show_menu(self):
        start_ollama()
        self.pet.hide()
        self.menu.show()


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    controller = AppController()
    controller.show_pet()
 
    #atexit.register(cleanup_ollama)
    sys.exit(app.exec())
