import sys
import signal
from PyQt5.QtWidgets import QApplication

from app.MainWindow import MainWindow

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()

