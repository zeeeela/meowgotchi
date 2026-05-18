import subprocess
import sys
import atexit

from PySide6.QtWidgets import QApplication, QStyleFactory

from meowgotchi.chat_page import ChatPage
from meowgotchi.pet import Pet
from meowgotchi.menu_page import MenuPage
from meowgotchi.research_page import ResearchChatPage
from meowgotchi.activity_page import ActivityPage

class AppController:
    def __init__(self):
        self.pet = Pet(on_to_menu=self.show_menu, on_to_research=self.show_research, on_to_chat=self.show_chat, on_to_activity=self.show_activity)
        self.menu = ChatPage(on_to_pet=self.show_pet)
        self.menuu = MenuPage()
        self.research_page = ResearchChatPage(on_to_pet=self.show_pet)
        self.activity_page = ActivityPage()

    def show_pet(self):
        cleanup_ollama()
        self.menu.hide()
        self.pet.show()
        self.menuu.hide()

    def show_menu(self):
        self.pet.show()
        self.menu.hide()
        self.menuu.show()

    def show_chat(self):
        start_ollama()
        self.menuu.hide()
        self.pet.show()
        self.menu.show()

    def show_research(self):
        start_ollama()
        self.research_page.show()
        self.pet.show()

    def show_activity(self):
        self.activity_page.show()
        self.pet.show()

def start_ollama():
    try:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Ollama server started.")
    except FileNotFoundError:
        print("Ollama not found. Please run 'ollama serve' manually.")
        sys.exit(1)

def cleanup_ollama():
    """Kill Ollama when app exits"""
    try:
        subprocess.run(["pkill", "-f", "ollama"], check=False)
        print("Ollama server stopped.")
    except FileNotFoundError:
        pass

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    controller = AppController()
    controller.show_pet()
 
    #atexit.register(cleanup_ollama)
    sys.exit(app.exec())
