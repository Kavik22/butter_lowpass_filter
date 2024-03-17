import sys, numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from scipy import signal
from second_ui import Ui_MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()

    sys.exit(app.exec())
