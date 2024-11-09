import numpy as np


class AudioProcessingTool:

    @staticmethod
    def calculate_energy(np_array):
        energy = np.sum(np.abs(np_array))
        return energy

    @staticmethod
    def calculate_sign_changes(np_array):
        array_positive = np_array > 0
        array_changes = np.diff(array_positive)
        num_changes = np.sum(array_changes != 0)
        return num_changes

    @staticmethod
    def calculate_fft(np_array, zoom_center_factor=10):

        num_samples = np_array.size
        zoom_last_sample = int(num_samples / (2 * zoom_center_factor))

        sp = np.fft.fft(np_array)

        fft = np.abs(sp.real[0:zoom_last_sample])
        return fft

