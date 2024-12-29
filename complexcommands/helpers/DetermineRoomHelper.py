from ai.video.ObjectDetector import ObjectDetector
from clients.CommandsClient import CommandsClient
from ai.video.Models import Models


class DetermineRoomHelper:

    instance = None

    @staticmethod
    def get_instance():
        if DetermineRoomHelper.instance is None:
            DetermineRoomHelper.instance = DetermineRoomHelper()

        return DetermineRoomHelper.instance

    def __init__(self):
        self.running = False
        self.last_image = None
        self.object_detector = ObjectDetector.load_custom_model("room_s_2024_12_28")
        self.commands_client = CommandsClient.get_instance()

    # FIXME finish
    # Models.MODEL_ROOM_DETECTION


