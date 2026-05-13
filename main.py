import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from poc import Pet


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    pet = Pet()
    pet.show()
    sys.exit(app.exec_())