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

        self.queue_of_chunks = queue.Queue()
        self.recognized_text = None

        # Start recognizing audio in a separate thread
        recognizing_thread = threading.Thread(target=self.process_audio_queue)
        recognizing_thread.start()

    def use_item_metadata_and_bytes(self, item_metadata, item_bytes):

        audio_chunk = item_bytes

        is_speech_detected = self.speech_detector.detect_voice(audio_chunk)

        if is_speech_detected:
            print("Speech detected!!")
            self.queue_of_chunks.put(audio_chunk)

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

            text = self.recognizer.recognize_google(audio_data)
            print(f"Recognized Text: {text}")

            if self.recognized_text is None:
                self.recognized_text = text
            else:
                self.recognized_text = self.recognized_text + " " + text

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            if self.recognized_text is not None:
                self.on_text_received_decoded(self.recognized_text)

                print("Back waiting for commands...")

                with self.queue_of_chunks.mutex:
                    self.queue_of_chunks.queue.clear()

            self.recognized_text = None

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            self.recognized_text = None

