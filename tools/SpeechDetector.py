import webrtcvad


class SpeechDetector:

    def __init__(self, aggressiveness=3):
        self.vad = webrtcvad.Vad(aggressiveness)

    @staticmethod
    def divide_bytearray(byte_array, piece_size):
        return [byte_array[i:i + piece_size] for i in range(0, len(byte_array), piece_size)]

    def detect_voice(self, audio_chunk):

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

