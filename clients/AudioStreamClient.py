from clients.AbstractStreamClient import AbstractStreamClient
from tools.SpeechDetector import SpeechDetector
import pyaudio
import threading
import queue
import speech_recognition as sr


class AudioStreamClient(AbstractStreamClient):

    def __init__(self, host, port, on_text_received_decoded):
        super().__init__(host, port)
        self.on_text_received_decoded = on_text_received_decoded
        self.speech_detector = SpeechDetector()

        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.rate = 16000
        self.audio_format = pyaudio.paInt16

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()

        self.queue_of_chunks = queue.Queue()
        self.list_chunk_parts = []

        # Start recognizing audio in a separate thread
        recognizing_thread = threading.Thread(target=self.process_audio_queue)
        recognizing_thread.start()

    def use_item_metadata_and_bytes(self, item_metadata, item_bytes):

        # Reception of audio chunks of 0.5 secs, from the first one that speech is detected until the last one with
        # detection, all them together will be sent to SpeechRecognition

        chunk_part = item_bytes

        is_speech_detected = self.speech_detector.detect_voice(chunk_part)

        if is_speech_detected:
            print("Speech detected!!")
            self.list_chunk_parts.append(chunk_part)

        else:

            if len(self.list_chunk_parts) > 0:
                audio_chunk = b''.join(self.list_chunk_parts)
                self.queue_of_chunks.put(audio_chunk)
                self.list_chunk_parts.clear()

    def process_audio_queue(self):

        try:
            while True:
                audio_chunk = self.queue_of_chunks.get()
                self.process_audio_chunk(audio_chunk)
                self.queue_of_chunks.task_done()

        except KeyboardInterrupt:
            print("Stopping audio capture...")

    def process_audio_chunk(self, audio_chunk):

        try:

            audio_data = sr.AudioData(audio_chunk, self.rate, self.p.get_sample_size(self.audio_format))

            recognized_text = self.recognizer.recognize_google(audio_data)
            print(f"Recognized Text: {recognized_text}")

            self.on_text_received_decoded(recognized_text)

            self.debug_print("Back waiting for commands...")

            with self.queue_of_chunks.mutex:
                self.queue_of_chunks.queue.clear()

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

