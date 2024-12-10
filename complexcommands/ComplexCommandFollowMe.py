from clients.CommandsClient import CommandsClient
from tools.CarMovement import CarMovement
from ai.video.Tracker import Tracker
from ai.video.ObjectDetector import ObjectDetector
import time


class ComplexCommandFollowMe:

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommandFollowMe.instance is None:
            ComplexCommandFollowMe.instance = ComplexCommandFollowMe()

        return ComplexCommandFollowMe.instance

    def __init__(self):
        self.running = False
        self.last_image = None
        self.commands_client = CommandsClient.get_instance()
        self.object_detector = ObjectDetector.load_standard_model("s")
        self.car_movement = CarMovement()
        self.tracker = Tracker(width, height, self.car_movement)

    def execute(self):

        self.running = True

        if not self.running:
            return

    # FIXME implement




