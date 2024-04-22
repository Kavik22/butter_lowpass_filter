import math

import numpy as np
import matplotlib.pyplot as plt


def amplitude_frequency_response(f, fc, n):
    F = f / fc
    amplitude = 1 / np.sqrt(1 + F ** (2 * n))
    return amplitude


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


def phase_frequency_response(f, fc, n):
    phase = (1 / math.sqrt(1 + (f / fc) ** (2 * n)))
    return phase

# frequency_cutoff = 500
# order = 4
#
# frequency = [f for f in range(0, 1500)]
# amplitude = [phase_frequency_response(f, frequency_cutoff, order) for f in frequency]
#
# plt.plot(amplitude, frequency)
# plt.show()
