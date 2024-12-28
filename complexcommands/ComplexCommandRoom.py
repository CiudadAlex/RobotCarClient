from ai.video.ObjectDetector import ObjectDetector
from clients.CommandsClient import CommandsClient


class ComplexCommandRoom:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandRoom.instance is None:
            ComplexCommandRoom.instance = ComplexCommandRoom()

        return ComplexCommandRoom.instance

    def __init__(self):
        self.running = False
        self.last_image = None
        self.object_detector = ObjectDetector.load_custom_model("room_s_20024_12_28")
        self.commands_client = CommandsClient.get_instance()

    def get_class(self, pil_image):

        self.running = True

        results = self.object_detector.predict(self.last_image)

        if results is None:
            continue

        most_confident_class = self.object_detector.get_most_confident_class(results)

        self.running = False

