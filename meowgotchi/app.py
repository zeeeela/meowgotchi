import sys

from PySide6.QtWidgets import QApplication, QStyleFactory

from meowgotchi.menu_page import MenuPage
from meowgotchi.pet import Pet


class AppController:
    def __init__(self):
        self.pet = Pet(on_to_menu=self.show_menu)
        self.menu = MenuPage(on_to_pet=self.show_pet)

    def show_pet(self):
        self.menu.hide()
        self.pet.show()

    def show_menu(self):
        self.pet.hide()
        self.menu.show()


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    controller = AppController()
    controller.show_pet()
    sys.exit(app.exec())
