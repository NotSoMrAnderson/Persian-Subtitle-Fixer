from subtitle_fixer_gui import MainWindow
from sys import argv, exit
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_()) 