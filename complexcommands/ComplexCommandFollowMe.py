from clients.CommandsClient import CommandsClient
from tools.CarMovement import CarMovement
from ai.video.Tracker import Tracker
from ai.video.ObjectDetector import ObjectDetector
from inforeception.CarInformationReceptor import CarInformationReceptor
import threading


class ComplexCommandFollowMe:

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommandFollowMe.instance is None:
            ComplexCommandFollowMe.instance = ComplexCommandFollowMe()

        return ComplexCommandFollowMe.instance

    def __init__(self):
        self.running = False
        self.commands_client = CommandsClient.get_instance()
        self.object_detector = ObjectDetector.load_standard_model("s")
        self.car_movement = CarMovement()
        self.tracker = Tracker(width=320, height=240, car_movement=self.car_movement)
        self.num_not_detections = 0

    def stop(self):
        self.running = False

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandFollowMe!!!!!!!")

        self.running = True

        self.commands_client.led_police()

        while self.running:

            last_image = CarInformationReceptor.get_instance().last_image
            results = self.object_detector.predict(last_image)

            if results is None:
                self.look_for_person_if_needed()
                continue

            bounding_box = self.object_detector.get_bounding_box_vertices_of_single_object_of_class(results, "person")

            if bounding_box is None:
                self.look_for_person_if_needed()
                continue

            rectangle_up_left_position = bounding_box[0]
            rectangle_down_right_position = bounding_box[1]
            self.tracker.track(rectangle_up_left_position, rectangle_down_right_position)
            self.num_not_detections = 0

        self.commands_client.led_stop()

    def look_for_person_if_needed(self):

        self.num_not_detections = self.num_not_detections + 1

        if self.num_not_detections > 3:
            self.car_movement.move_right()
            self.num_not_detections = 0
