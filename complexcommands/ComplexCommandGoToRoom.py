from clients.CommandsClient import CommandsClient
from ai.video.ObjectDetector import ObjectDetector
import threading


class ComplexCommandGoToRoom:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandGoToRoom.instance is None:
            ComplexCommandGoToRoom.instance = ComplexCommandGoToRoom()

        return ComplexCommandGoToRoom.instance

    def __init__(self):
        self.running = False
        self.last_image = None
        self.commands_client = CommandsClient.get_instance()
        self.object_detector = ObjectDetector.load_custom_model("room_s_2024_12_28")

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandGoToRoom!!!!!!!")

        self.running = True

        self.running = False

