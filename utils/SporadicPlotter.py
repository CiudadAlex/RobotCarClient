import time
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
