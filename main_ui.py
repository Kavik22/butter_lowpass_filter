from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                          QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                         QFont, QFontDatabase, QGradient, QIcon,
                         QImage, QKeySequence, QLinearGradient, QPainter,
                         QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QSizePolicy, QStatusBar,
                             QWidget, QGraphicsScene, QVBoxLayout)
from scipy import signal
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class GraphicWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Butterworth graphic")
        self.resize(700, 500)

        order_text = parent.order_input.text()
        frequency_text = parent.frequency_input.text()

        if str(order_text).isdigit() and str(frequency_text).isdigit():
            order = int(parent.order_input.text())
            frequency = int(parent.frequency_input.text())

            b, a = signal.butter(order, frequency, 'low', analog=True)
            w, h = signal.freqs(b, a)

            self.figure = plt.Figure()
            self.canvas = FigureCanvas(self.figure)
            self.setCentralWidget(self.canvas)
            self.figure.clear()

            ax = self.figure.add_subplot(111)

            ax.semilogx(w, 20 * np.log10(abs(h)))
            ax.set_title('Butterworth filter frequency response')
            ax.set_xlabel('Frequency [radians / second]')
            ax.set_ylabel('Amplitude [dB]')
            ax.margins(0, 0.1)
            ax.grid(which='both', axis='both')
            ax.axvline(100, color='green')  # cutoff frequency

            self.canvas.draw()


class FilterWindow(QMainWindow):
    def __init__(self):
        super(FilterWindow, self).__init__()

        self.resize(800, 570)
        self.setStyleSheet(u"background-color:  rgb(200, 200, 200)")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")

        self.order_label = QLabel(self.centralwidget)
        self.order_label.setObjectName(u"order_label")
        self.order_label.setGeometry(QRect(60, 60, 171, 21))
        self.frequency_label = QLabel(self.centralwidget)
        self.frequency_label.setObjectName(u"frequency_label")
        self.frequency_label.setGeometry(QRect(60, 90, 211, 21))
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(60, 16, 631, 31))
        self.graph_create_button = QPushButton(self.centralwidget)
        self.graph_create_button.setObjectName(u"graph_create_button")
        self.graph_create_button.setGeometry(QRect(530, 60, 211, 51))
        font = QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.graph_create_button.setFont(font)
        self.graph_create_button.clicked.connect(self.create_graphic_window)
        self.order_input = QLineEdit(self.centralwidget)
        self.order_input.setObjectName(u"order_input")
        self.order_input.setGeometry(QRect(290, 60, 61, 25))
        self.frequency_input = QLineEdit(self.centralwidget)
        self.frequency_input.setObjectName(u"frequency_input")
        self.frequency_input.setGeometry(QRect(290, 90, 61, 25))
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.order_label.setText(QCoreApplication.translate("MainWindow",
                                                            u"<html><head/><body><p><span style=\" font-size:14pt;\">\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0444\u0438\u043b\u044c\u0442\u0440\u0430:</span></p></body></html>",
                                                            None))
        self.frequency_label.setText(QCoreApplication.translate("MainWindow",
                                                                u"<html><head/><body><p><span style=\" font-size:14pt;\">\u0427\u0430\u0441\u0442\u043e\u0442\u0430 \u0441\u0440\u0435\u0437\u0430 \u0432 \u0433\u0435\u0440\u0446\u0430\u0445:</span></p></body></html>",
                                                                None))
        self.title.setText(QCoreApplication.translate("MainWindow",
                                                      u"<html><head/><body><p><span style=\" font-size:20pt;\">\u0424\u0438\u043b\u044c\u0442\u0440 \u043d\u0438\u0437\u043a\u0438\u0445 \u0447\u0430\u0441\u0442\u043e\u0442 \u0411\u0430\u0442\u0442\u0435\u0440\u0432\u043e\u0440\u0442\u0430</span></p></body></html>",
                                                      None))
        self.graph_create_button.setText(QCoreApplication.translate("MainWindow",
                                                                    u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a",
                                                                    None))

    def create_graphic_window(self):
        self.window = GraphicWindow(self)
        self.window.show()
