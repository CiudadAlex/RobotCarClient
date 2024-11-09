import webrtcvad
import numpy as np
import wave
import pyaudio
from utils.SporadicPlotter import SporadicPlotter


class SpeechDetector:

    def __init__(self, aggressiveness=0, debug=True):
        self.vad = webrtcvad.Vad(aggressiveness)
        self.debug = debug
        self.chans = 1
        self.rate = 16000
        self.audio_format = pyaudio.paInt16

        self.p = pyaudio.PyAudio()
        self.idx = 0
        self.sporadic_plotter = SporadicPlotter(secs_between_plots=5)

    @staticmethod
    def divide_bytearray(byte_array, piece_size):
        return [byte_array[i:i + piece_size] for i in range(0, len(byte_array), piece_size)]

    def analyze_audio(self, chunk):

        np_array = np.frombuffer(chunk, dtype=np.int16)
        energy = self.calculate_energy(np_array)
        sign_changes = self.calculate_sign_changes(np_array)

        if self.debug:
            print(f"energy = {energy}")
            print(f"sign_changes = {sign_changes}")

        # self.store_audio_file(chunk)
        # self.sporadic_plotter.plot(np_array)

        self.sporadic_plotter.plot_fft(np_array)

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

    def store_audio_file(self, audio_chunk):

        self.idx = self.idx + 1

        # creates wave file with audio read in
        # Code is from the wave file audio tutorial as referenced below
        wav_output_filename = f'test{self.idx}.wav'
        wavefile = wave.open(wav_output_filename, 'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(self.p.get_sample_size(self.audio_format))
        wavefile.setframerate(self.rate)
        wavefile.writeframes(audio_chunk)
        wavefile.close()

    def detect_voice(self, audio_chunk):

        # Divide in segments of 30 ms (mandatory for VAD)
        frame_duration = 30 / 1000  # secs
        sample_rate = 16000
        bytes_per_sample = 2
        piece_size = int(bytes_per_sample * sample_rate * frame_duration)

        list_frames = self.divide_bytearray(audio_chunk, piece_size)
        # self.analyze_audio(audio_chunk)

        # Evaluate each frame to detect speech
        is_speech_detected = False
        for frame in list_frames:

            if self.vad.is_speech(frame, sample_rate):
                is_speech_detected = True
                break

        return is_speech_detected

