import numpy as np
import matplotlib.pyplot as plt


def frequency_response(f, fc, n):
    F = f / fc
    amplitude = 1 / np.sqrt(1 + F ** (2 * n))
    return amplitude


def frequency_response_check():
    fc = 50
    n = 5

    frequency = [f for f in range(0, 1000)]
    amplitude = [20 * np.log10(frequency_response(f, fc, n)) for f in frequency]

    plt.semilogx(frequency, amplitude)
    plt.title('Butterworth filter frequency response')
    plt.xlabel('Frequency [radians / second]')
    plt.ylabel('Amplitude [dB]')
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.axvline(fc, color='green')  # cutoff frequency

    plt.show()


def raw_element(n, m):
    raw = 2 * np.sin((2 * m - 1) * np.pi / (2 * n))
    return raw


def c(n, wc, r, m):
    result = raw_element(n, m) / (r * wc)
    return result


def l(n, wc, r, m):
    result = raw_element(n, m) * r / wc
    return result


def elements_for_p_type():
    n = 5
    fc = 100
    r = 1000
    wc = 2 * np.pi * fc
    for m in range(1, n + 1):
        if m % 2 != 0:
            print(f'C({m}) = {c(n, wc, r, m)}')
        else:
            print(f'L({m}) = {l(n, wc, r, m)}')


def elements_for_t_type():
    n = 5
    fc = 100
    r = 1000
    wc = 2 * np.pi * fc
    for m in range(1, n + 1):
        if m % 2 != 0:
            print(f'L({m}) = {l(n, wc, r, m)}')
        else:
            print(f'C({m}) = {c(n, wc, r, m)}')


if __name__ == '__main__':
    # elements_for_p_type()
    # print('--------------')
    # elements_for_t_type()
    frequency_response_check()
