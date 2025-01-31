from ai.video.ObjectDetector import ObjectDetector
from clients.CommandsClient import CommandsClient
from ai.video.Models import Models
from utils.Aggregator import Aggregator
from inforeception.CarInformationReceptor import CarInformationReceptor
import time


class DetermineRoomHelper:

    number_of_steps = 10

    time_sleep_move = 0.25
    time_sleep_adjust_image = 1.5

    instance = None

    @staticmethod
    def get_instance():
        if DetermineRoomHelper.instance is None:
            DetermineRoomHelper.instance = DetermineRoomHelper()

        return DetermineRoomHelper.instance

    def __init__(self):
        self.running = False
        self.object_detector = ObjectDetector.load_custom_model(Models.MODEL_ROOM_DETECTION)
        self.commands_client = CommandsClient.get_instance()

    def stop(self):
        self.running = False

    def get_room(self):

        self.running = True
        confidence_aggregator = Aggregator()

        for step in range(DetermineRoomHelper.number_of_steps):

            if not self.running:
                return confidence_aggregator.get_max_count()

            self.move_step()
            self.aggregate_confidence_of_classes_of_last_image(confidence_aggregator)

        most_confident_class = confidence_aggregator.get_key_of_max_value()

        self.running = False

        return most_confident_class

    def aggregate_confidence_of_classes_of_last_image(self, confidence_aggregator):

        last_image = CarInformationReceptor.get_instance().last_image
        results = self.object_detector.predict(last_image)
        list_class_and_confidence = self.object_detector.get_list_class_and_confidence(results)

        detected_class_set = set()

        for clazz, confidence in list_class_and_confidence:

            if clazz not in detected_class_set:
                confidence_aggregator.add(clazz, confidence)
                detected_class_set.add(clazz)

    def move_step(self):

        self.commands_client.move_turn_left()
        time.sleep(DetermineRoomHelper.time_sleep_move)
        self.commands_client.move_stop()
        time.sleep(DetermineRoomHelper.time_sleep_adjust_image)

