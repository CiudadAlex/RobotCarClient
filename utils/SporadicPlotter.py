import time
import numpy as np
import matplotlib.pyplot as plt


class SporadicPlotter:

    def __init__(self, secs_between_plots=5):
        self.secs_between_plots = secs_between_plots
        self.last_time_plotted = 0

    def plot(self, np_array):

        now = time.time()

        if now - self.last_time_plotted < self.secs_between_plots:
            return

        plt.plot(np_array)
        plt.show()

        plt.figure()

        self.last_time_plotted = time.time()

    def plot_fft(self, np_array):

        now = time.time()

        if now - self.last_time_plotted < self.secs_between_plots:
            return

        t = np.arange(np_array.size)
        sp = np.fft.fft(np_array)
        freq = np.fft.fftfreq(t.shape[-1])

        plt.plot(freq, sp.real, freq, sp.imag)
        plt.show()

        plt.figure()

        self.last_time_plotted = time.time()
