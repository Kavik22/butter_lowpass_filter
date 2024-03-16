from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                          QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                         QFont, QFontDatabase, QGradient, QIcon,
                         QImage, QKeySequence, QLinearGradient, QPainter,
                         QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QSizePolicy, QWidget)
from scipy import signal
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class AFGraphicWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Butterworth graphic")
        self.resize(700, 500)

        order_text = parent.order_input.text()
        frequency_text = parent.frequency_input.text()

        if str(order_text).isdigit() and str(frequency_text).isdigit():
            order = int(order_text)
            frequency = int(frequency_text)

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
            ax.axvline(frequency, color='green')  # cutoff frequency

            self.canvas.draw()


class ATGraphicWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Butterworth graphic")
        self.resize(700, 500)

        order_text = parent.order_input.text()
        frequency_text = parent.frequency_input.text()
        frequency_sampling_text = parent.frequency_sampling_input.text()

        if str(order_text).isdigit() and str(frequency_text).isdigit() and str(frequency_sampling_text).isdigit():
            order = int(order_text)
            frequency = int(frequency_text)
            frequency_sampling = int(frequency_sampling_text)

            t = np.linspace(0, 1, int(frequency_sampling))
            data = np.sin(2 * np.pi * 100 * t) + 0.7 * np.sin(2 * np.pi * 200 * t)

            def butter_lowpass(cutoff, fs, order=5):
                nyquist = 0.5 * fs
                normal_cutoff = cutoff / nyquist
                b, a = signal.butter(order, normal_cutoff, btype='low', analog=True)
                return b, a

            def butter_lowpass_filter(data, cutoff, fs, order=5):
                b, a = butter_lowpass(cutoff, fs, order=order)
                y = signal.lfilter(b, a, data)
                return y

            filtered_data = butter_lowpass_filter(data, frequency, frequency_sampling, order)

            self.figure = plt.Figure()
            self.canvas = FigureCanvas(self.figure)
            self.setCentralWidget(self.canvas)
            self.figure.clear()

            ax = self.figure.add_subplot(111)

            ax.plot(t, data, 'b-', label='Original signal')
            ax.plot(t, filtered_data, 'r-', linewidth=2, label='Filtered signal')
            ax.set_xlabel('Time [second]')
            ax.set_ylabel('Amplitude [dB]')
            ax.set_title('Butterworth low pass filter')
            ax.legend()
            ax.grid(which='both', axis='both')

            self.canvas.draw()


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.resize(512, 314)
        self.setStyleSheet(u"background-color:  rgb(200, 200, 200);")
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
        self.title.setGeometry(QRect(30, 10, 451, 31))
        self.af_graph_create_button = QPushButton(self.centralwidget)
        self.af_graph_create_button.setObjectName(u"graph_create_button")
        self.af_graph_create_button.setGeometry(QRect(30, 170, 451, 51))
        self.af_graph_create_button.clicked.connect(self.create_af_graphic_window)
        font = QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.af_graph_create_button.setFont(font)
        self.order_input = QLineEdit(self.centralwidget)
        self.order_input.setObjectName(u"order_input")
        self.order_input.setGeometry(QRect(390, 60, 61, 25))
        self.frequency_input = QLineEdit(self.centralwidget)
        self.frequency_input.setObjectName(u"frequency_input")
        self.frequency_input.setGeometry(QRect(390, 90, 61, 25))
        self.frequency_sampling_label = QLabel(self.centralwidget)
        self.frequency_sampling_label.setObjectName(u"frequency_sampling_label")
        self.frequency_sampling_label.setGeometry(QRect(60, 120, 301, 21))
        self.frequency_sampling_input = QLineEdit(self.centralwidget)
        self.frequency_sampling_input.setObjectName(u"frequency_sampling_input")
        self.frequency_sampling_input.setGeometry(QRect(390, 120, 61, 25))
        self.at_graph_create_button = QPushButton(self.centralwidget)
        self.at_graph_create_button.setObjectName(u"graph_create_button_2")
        self.at_graph_create_button.setGeometry(QRect(30, 230, 451, 51))
        self.at_graph_create_button.setFont(font)
        self.at_graph_create_button.clicked.connect(self.create_at_graphic_window)

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
        self.af_graph_create_button.setText(QCoreApplication.translate("MainWindow",
                                                                       u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a \u0430\u043c\u043f\u043b\u0438\u0442\u0443\u0434\u044b \u043e\u0442 \u0447\u0430\u0441\u0442\u043e\u0442\u044b",
                                                                       None))
        self.frequency_sampling_label.setText(QCoreApplication.translate("MainWindow",
                                                                         u"<html><head/><body><p><span style=\" font-size:14pt;\">\u0427\u0430\u0441\u0442\u043e\u0442\u0430 \u0434\u0438\u0441\u043a\u0440\u0435\u0442\u0438\u0437\u0430\u0446\u0438\u0438 \u0432 \u0433\u0435\u0440\u0446\u0430\u0445:</span></p></body></html>",
                                                                         None))
        self.at_graph_create_button.setText(QCoreApplication.translate("MainWindow",
                                                                       u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a \u0430\u043c\u043f\u043b\u0438\u0442\u0443\u0434\u044b \u043e\u0442 \u0432\u0440\u0435\u043c\u0435\u043d\u0438",
                                                                       None))

    def create_af_graphic_window(self):
        self.window = AFGraphicWindow(self)
        self.window.show()

    def create_at_graphic_window(self):
        self.window = ATGraphicWindow(self)
        self.window.show()
