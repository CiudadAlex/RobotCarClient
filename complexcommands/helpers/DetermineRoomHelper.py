from ai.video.ObjectDetector import ObjectDetector
from clients.CommandsClient import CommandsClient
from ai.video.Models import Models
from utils.Counter import Counter
from inforeception.CarInformationReceptor import CarInformationReceptor
import time


class DetermineRoomHelper:

    number_of_steps = 5

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
        counter = Counter()

        for step in range(DetermineRoomHelper.number_of_steps):

            if not self.running:
                return counter.get_max_count()

            self.move_step()
            last_image_class = self.get_class_of_last_image()
            counter.add(last_image_class)

        most_confident_class = counter.get_max_count()

        self.running = False

        return most_confident_class

    def get_class_of_last_image(self):

        last_image = CarInformationReceptor.get_instance().last_image
        results = self.object_detector.predict(last_image)
        most_confident_class = self.object_detector.get_most_confident_class(results)
        return most_confident_class

    def move_step(self):

        self.commands_client.move_turn_left()
        time.sleep(DetermineRoomHelper.time_sleep_move)
        self.commands_client.move_stop()
        time.sleep(DetermineRoomHelper.time_sleep_adjust_image)

