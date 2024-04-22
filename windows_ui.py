from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                          QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                         QFont, QFontDatabase, QGradient, QIcon,
                         QImage, QKeySequence, QLinearGradient, QPainter,
                         QPalette, QPixmap, QRadialGradient, QTransform, QPixmap)
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QSizePolicy, QWidget, QScrollArea, QTextEdit, QVBoxLayout, QHBoxLayout,
                             QLayout, QComboBox, QTabWidget)
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from logic import amplitude_frequency_response, phase_frequency_response, c, l


class AFGraphicWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Frequency response graphic")
        self.resize(700, 500)

        order_text = parent.order_input.text()
        frequency_cutoff_text = parent.frequency_input.text()

        if str(order_text).isdigit() and str(frequency_cutoff_text).isdigit():
            order = int(order_text)
            frequency_cutoff = int(frequency_cutoff_text)

            frequency = [f for f in range(0, frequency_cutoff**2)]
            amplitude = [20 * np.log10(amplitude_frequency_response(f, frequency_cutoff, order)) for f in frequency]

            self.figure = plt.Figure()
            self.canvas = FigureCanvas(self.figure)
            self.setCentralWidget(self.canvas)
            self.figure.clear()

            ax = self.figure.add_subplot(111)

            ax.semilogx(frequency, amplitude)
            ax.set_title('Butterworth filter frequency response')
            ax.set_xlabel('Frequency [radians / second]')
            ax.set_ylabel('Amplitude [dB]')
            ax.margins(0, 0.1)
            ax.grid(which='both', axis='both')
            ax.axvline(frequency_cutoff, color='green')  # cutoff frequency

            self.canvas.draw()

class PFGraphicWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Phase frequency response graphic")
        self.resize(700, 500)

        order_text = parent.order_input.text()
        frequency_cutoff_text = parent.frequency_input.text()

        if str(order_text).isdigit() and str(frequency_cutoff_text).isdigit():
            order = int(order_text)
            frequency_cutoff = int(frequency_cutoff_text)

            frequency = [f for f in range(0, frequency_cutoff*3)]
            phase = [phase_frequency_response(f, frequency_cutoff, order) for f in frequency]

            self.figure = plt.Figure()
            self.canvas = FigureCanvas(self.figure)
            self.setCentralWidget(self.canvas)
            self.figure.clear()

            ax = self.figure.add_subplot(111)

            ax.plot(frequency, phase)
            ax.set_title('Butterworth filter frequency response')
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Phase')
            ax.margins(0, 0.1)
            ax.grid(which='both', axis='both')
            # ax.axvline(frequency_cutoff, color='green')  # cutoff frequency

            self.canvas.draw()

class CalculationOfElementsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculation of elements")

        self.resize(580, 480)
        self.setStyleSheet(u"background-color:  rgb(200, 200, 200);")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(30, 10, 520, 31))

        order_text = parent.order_input.text()
        frequency_cutoff_text = parent.frequency_input.text()
        resist_input_text = parent.resist_input.text()
        schema_type = parent.schema_type_input.currentText()

        if str(order_text).isdigit() and str(frequency_cutoff_text).isdigit() and str(resist_input_text).isdigit():
            order = int(order_text)
            frequency_cutoff = int(frequency_cutoff_text)
            resist = int(resist_input_text)
            wc = 2 * np.pi * frequency_cutoff

            c_array = []
            l_array = []

            for m in range(1, order + 1):
                if m % 2 == 0 and schema_type == 'П-образная' or m % 2 != 0 and schema_type == 'T-образная':
                    l_temp = l(order, wc, resist, m)
                    power = int(np.log10(l_temp))
                    if power < 0:
                        l_array.append(f'L({m}) = {np.round(l_temp / 10 ** (power - 1), 3)} * 10^{power - 1} Гн')
                    else:
                        l_array.append(f'L({m}) = {np.round(l_temp, 3)} Гн')
                else:
                    c_temp = c(order, wc, resist, m)
                    power = int(np.log10(c_temp))
                    if power < 0:
                        c_array.append(f'C({m}) = {np.round(c_temp / 10 ** (power - 1), 3)} * 10^{power - 1} Ф')
                    else:
                        c_array.append(f'C({m}) = {np.round(c_temp, 3)} Ф')

            l_text = '\n'.join(l_array)
            c_text = '\n'.join(c_array)

            self.c_elements_text = QTextEdit(self.centralwidget)
            self.c_elements_text.setPlainText(c_text)
            self.c_elements_text.setReadOnly(True)
            self.c_elements_text.setGeometry(20, 60, 270, 150)
            self.c_elements_text.setFont(QFont("AnyStyle", 14))
            self.l_elements_text = QTextEdit(self.centralwidget)
            self.l_elements_text.setPlainText(l_text)
            self.l_elements_text.setReadOnly(True)
            self.l_elements_text.setGeometry(290, 60, 270, 150)
            self.l_elements_text.setFont(QFont("AnyStyle", 14))

            self.order_label = QLabel(self.centralwidget)
            self.order_label.setObjectName(u"order_label")
            self.order_label.setGeometry(QRect(40, 230, 500, 21))
            self.order_label.setText(f'Порядок фильтра: {order}')
            self.order_label.setFont(QFont("AnyStyle", 14))
            self.frequency_label = QLabel(self.centralwidget)
            self.frequency_label.setObjectName(u"frequency_label")
            self.frequency_label.setGeometry(QRect(40, 260, 500, 21))
            self.frequency_label.setText(f'Частота среза в Герцах: {frequency_cutoff}')
            self.frequency_label.setFont(QFont("AnyStyle", 14))
            self.resist_label = QLabel(self.centralwidget)
            self.resist_label.setObjectName(u"resist_label")
            self.resist_label.setGeometry(QRect(40, 290, 500, 21))
            self.resist_label.setText(f'Сопротивление в Омах: {resist}')
            self.resist_label.setFont(QFont("AnyStyle", 14))
            self.schema_type_label = QLabel(self.centralwidget)
            self.schema_type_label.setObjectName(u"schema_type_label")
            self.schema_type_label.setGeometry(QRect(40, 320, 500, 21))
            self.schema_type_label.setText(f'Тип схемы: {schema_type}')
            self.schema_type_label.setFont(QFont("AnyStyle", 14))

            self.image_label = QLabel(self.centralwidget)
            if schema_type == 'П-образная':
                pixmap = QPixmap('Pscheme.png')
            else:
                pixmap = QPixmap('Tscheme.png')
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.image_label.setGeometry(30, 350, int(pixmap.width() / 3), int(pixmap.height() / 3))

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("CalculationOfElements", u"CalculationOfElements", None))
        self.title.setText(QCoreApplication.translate("MainWindow",
                                                      u"<html><head/><body><p><span style=\" font-size:20pt;\">\u0420\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043D\u043D\u044B\u0435\u0020\u0437\u043D\u0430\u0447\u0435\u043D\u0438\u044F\u0020\u044D\u043B\u0435\u043C\u0435\u043D\u0442\u043E\u0432\u0020\u0446\u0435\u043F\u0438</span></p></body></html>",
                                                      None))


class Manual_Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Инструкция по эксплуатации")

        pixmap_user_guide = QPixmap('userguide.png')

        self.resize(1333, 753)
        self.setStyleSheet(u"background-color:  rgb(255, 255, 255);")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")

        self.user_guide_image_label = QLabel(self.centralwidget)
        self.user_guide_image_label.setPixmap(pixmap_user_guide)
        self.user_guide_image_label.setScaledContents(True)
        self.user_guide_image_label.setFixedSize(int(pixmap_user_guide.width() / 1.5), int(pixmap_user_guide.height() / 1.5))
        # self.image_label.setGeometry(0, 0, int(pixmap.width() / 1.5), int(pixmap.height() / 1.5))

        pixmap_second = QPixmap('info.png')
        self.image_label = QLabel(self.centralwidget)
        self.image_label.setPixmap(pixmap_second)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(int(pixmap_second.width() / 1.5), int(pixmap_second.height() / 1.5))

        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.addTab(self.user_guide_image_label, 'Пользовательская инструкция')
        self.tabs.addTab(self.image_label, 'Принципы рассчёта АЧХ и значений элементов цепи')


        self.setCentralWidget(self.centralwidget)






class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.resize(570, 394)
        self.setStyleSheet(u"background-color:  rgb(200, 200, 200);")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.order_label = QLabel(self.centralwidget)
        self.order_label.setObjectName(u"order_label")
        self.order_label.setGeometry(QRect(40, 60, 171, 21))
        self.frequency_label = QLabel(self.centralwidget)
        self.frequency_label.setObjectName(u"frequency_label")
        self.frequency_label.setGeometry(QRect(40, 90, 211, 21))
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(40, 10, 451, 31))
        self.af_graph_create_button = QPushButton(self.centralwidget)
        self.af_graph_create_button.setObjectName(u"graph_create_button")
        self.af_graph_create_button.setGeometry(QRect(60, 190, 451, 51))
        self.af_graph_create_button.clicked.connect(self.create_af_graphic_window)
        self.manual_button = QPushButton(self.centralwidget)
        self.manual_button.setObjectName(u"manual_button")
        self.manual_button.setGeometry(QRect(500, 10, 30, 30))
        self.manual_button.clicked.connect(self.manual_window)
        self.manual_button.setText('?')
        self.manual_button.setFont(QFont('AnyStyle', 16))
        font = QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.af_graph_create_button.setFont(font)
        self.order_input = QLineEdit(self.centralwidget)
        self.order_input.setObjectName(u"order_input")
        self.order_input.setGeometry(QRect(470, 60, 61, 25))
        self.frequency_input = QLineEdit(self.centralwidget)
        self.frequency_input.setObjectName(u"frequency_input")
        self.frequency_input.setGeometry(QRect(470, 90, 61, 25))
        self.resist_label = QLabel(self.centralwidget)
        self.resist_label.setObjectName(u"frequency_sampling_label")
        self.resist_label.setGeometry(QRect(40, 120, 421, 21))
        self.resist_input = QLineEdit(self.centralwidget)
        self.resist_input.setObjectName(u"frequency_sampling_input")
        self.resist_input.setGeometry(QRect(470, 120, 61, 25))
        self.calculate_of_elements_create_button = QPushButton(self.centralwidget)
        self.calculate_of_elements_create_button.setObjectName(u"calculate_of_elements_create_button")
        self.calculate_of_elements_create_button.setGeometry(QRect(60, 310, 451, 51))
        self.calculate_of_elements_create_button.setFont(font)
        self.calculate_of_elements_create_button.clicked.connect(self.calculate_of_elements_window)


        self.pf_graph_create_button = QPushButton(self.centralwidget)
        self.pf_graph_create_button.setObjectName(u"calculate_of_elements_create_button")
        self.pf_graph_create_button.setGeometry(QRect(60, 250, 451, 51))
        self.pf_graph_create_button.setFont(font)
        self.pf_graph_create_button.setText('Построить график фазы от частоты')
        self.pf_graph_create_button.clicked.connect(self.create_pf_graphic_window)


        self.schema_type_label = QLabel(self.centralwidget)
        self.schema_type_label.setObjectName(u"order_label")
        self.schema_type_label.setGeometry(QRect(40, 150, 421, 21))
        self.schema_type_label.setText(f'Тип схемы:')
        self.schema_type_label.setFont(QFont("AnyStyle", 14))
        self.schema_type_input = QComboBox(self.centralwidget)
        self.schema_type_input.addItem('П-образная')
        self.schema_type_input.addItem('T-образная')
        self.schema_type_input.setGeometry(160, 150, 120, 25)
        self.schema_type_input.setCurrentIndex(0)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.order_label.setText(QCoreApplication.translate("MainWindow",
                                                            u"<html><head/><body><p><span style=\" font-size:14pt;\">\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0444\u0438\u043b\u044c\u0442\u0440\u0430:</span></p></body></html>",
                                                            None))
        self.frequency_label.setText(QCoreApplication.translate("MainWindow",
                                                                u"<html><head/><body><p><span style=\" font-size:14pt;\">\u0427\u0430\u0441\u0442\u043E\u0442\u0430\u0020\u0441\u0440\u0435\u0437\u0430\u0020\u0432\u0020\u0413\u0435\u0440\u0446\u0430\u0445:</span></p></body></html>",
                                                                None))
        self.title.setText(QCoreApplication.translate("MainWindow",
                                                      u"<html><head/><body><p><span style=\" font-size:20pt;\">\u0424\u0438\u043b\u044c\u0442\u0440 \u043d\u0438\u0437\u043a\u0438\u0445 \u0447\u0430\u0441\u0442\u043e\u0442 \u0411\u0430\u0442\u0442\u0435\u0440\u0432\u043e\u0440\u0442\u0430</span></p></body></html>",
                                                      None))
        self.af_graph_create_button.setText(QCoreApplication.translate("MainWindow",
                                                                       u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a \u0430\u043c\u043f\u043b\u0438\u0442\u0443\u0434\u044b \u043e\u0442 \u0447\u0430\u0441\u0442\u043e\u0442\u044b",
                                                                       None))
        self.resist_label.setText(QCoreApplication.translate("MainWindow",
                                                             u"<html><head/><body><p><span style=\" font-size:14pt;\">\u0421\u043E\u043F\u0440\u043E\u0442\u0438\u0432\u043B\u0435\u043D\u0438\u0435\u0020\u043D\u0430\u0433\u0440\u0443\u0437\u043A\u0438\u0020\u0438\u0020\u0438\u0441\u0442\u043E\u0447\u043D\u0438\u043A\u0430\u0020\u0432\u0020\u041E\u043C\u0430\u0445:</span></p></body></html>",
                                                             None))
        self.calculate_of_elements_create_button.setText(QCoreApplication.translate("MainWindow",
                                                                                    u"\u0420\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u0442\u044C\u0020\u0437\u043D\u0430\u0447\u0435\u043D\u0438\u044F\u0020\u044D\u043B\u0435\u043C\u0435\u043D\u0442\u043E\u0432\u0020\u0446\u0435\u043F\u0438",
                                                                                    None))

    def create_af_graphic_window(self):
        self.window = AFGraphicWindow(self)
        self.window.show()

    def create_pf_graphic_window(self):
        self.window = PFGraphicWindow(self)
        self.window.show()

    def calculate_of_elements_window(self):
        self.window = CalculationOfElementsWindow(self)
        self.window.show()

    def manual_window(self):
        self.window = Manual_Window(self)
        self.window.show()
