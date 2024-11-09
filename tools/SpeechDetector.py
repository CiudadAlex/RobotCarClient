import webrtcvad
import numpy as np
import wave
import pyaudio
from utils.SporadicPlotter import SporadicPlotter
from tools.AudioProcessingTool import AudioProcessingTool


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

    def is_speech(self, chunk):

        np_array = np.frombuffer(chunk, dtype=np.int16)
        fft = AudioProcessingTool.calculate_fft(np_array, zoom_center_factor=10)
        fft = fft[100:]

        energy = AudioProcessingTool.calculate_energy(fft)

        if self.debug:
            plotted = self.sporadic_plotter.plot(fft)
            if plotted:
                print(f"energy = {energy}")
                # self.store_audio_file(chunk)

        return energy > 120

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
        return self.is_speech(audio_chunk)

    def detect_voice_vad(self, audio_chunk):

        # Divide in segments of 30 ms (mandatory for VAD)
        frame_duration = 30 / 1000  # secs
        sample_rate = 16000
        bytes_per_sample = 2
        piece_size = int(bytes_per_sample * sample_rate * frame_duration)

        list_frames = self.divide_bytearray(audio_chunk, piece_size)

        # Evaluate each frame to detect speech
        is_speech_detected = False
        for frame in list_frames:

            if self.vad.is_speech(frame, sample_rate):
                is_speech_detected = True
                break

        return is_speech_detected

