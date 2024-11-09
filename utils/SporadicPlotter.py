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

    def plot_fft(self, np_array, zoom_center_factor=30):

        now = time.time()

        if now - self.last_time_plotted < self.secs_between_plots:
            return

        self.last_time_plotted = time.time()

        num_samples = np_array.size
        zoom_last_sample = int(num_samples / (2 * zoom_center_factor))

        sp = np.fft.fft(np_array)

        fft = np.abs(sp.real[0:zoom_last_sample])

        plt.plot(fft)
        plt.show()

        plt.figure()





