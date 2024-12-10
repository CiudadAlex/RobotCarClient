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
        self.tracker = Tracker(width=320, height=240, car_movement=self.car_movement)

    def execute(self):

        self.running = True

        while self.running:

            results = self.object_detector.predict(self.last_image)
            point1, point2 = self.object_detector.get_bounding_box_vertices_of_single_object_of_class(results, "person")

            rectangle_up_left_position = point1
            rectangle_down_right_position = point2
            self.tracker.track(rectangle_up_left_position, rectangle_down_right_position)

    # FIXME implement




