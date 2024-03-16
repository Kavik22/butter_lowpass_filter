import sys, numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtCore import Slot
from main_ui import FilterWindow
from scipy import signal

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FilterWindow()
    window.show()

    sys.exit(app.exec())
