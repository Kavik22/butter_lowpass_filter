import sys, numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtCore import Slot
# from main_ui import FilterWindow
from scipy import signal
from second_ui import Ui_MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()

    sys.exit(app.exec())
