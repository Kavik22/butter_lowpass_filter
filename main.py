import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz


def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=True)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Пример данных (замените на свои)
fs = 150.0  # Частота дискретизации
cutoff = 50.0  # Частота среза (в Гц)

# Генерируем синусоидальный сигнал
t = np.linspace(0, 1, int(fs))
data = np.sin(2 * np.pi * 100 * t) + 0.7 * np.sin(2 * np.pi * 200 * t)

# Применяем фильтр
filtered_data = butter_lowpass_filter(data, cutoff, fs)

print(filtered_data)
# Визуализация
plt.figure()
plt.plot(t, data, 'b-', label='Исходный сигнал')
plt.plot(t, filtered_data, 'r-', linewidth=2, label='Фильтрованный сигнал')
plt.xlabel('Время (сек)')
plt.ylabel('Амплитуда')
plt.title('Фильтр низких частот Баттерворта')
plt.legend()
plt.grid(True)
plt.show()
