from ai.video.ObjectDetector import ObjectDetector
from clients.CommandsClient import CommandsClient
from utils.Counter import Counter
import time


class ComplexCommandRoom:

    number_of_steps = 5

    time_sleep_move = 0.25
    time_sleep_adjust_image = 1.5

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

    def execute(self):

        print("ComplexCommandRoom!!!!!!!")

        self.running = True
        counter = Counter()

        for step in range(ComplexCommandRoom.number_of_steps):

            if not self.running:
                return

            self.move_step()
            last_image_class = self.get_class_of_last_image()
            counter.add(last_image_class)

        most_confident_class = counter.get_max_count()
        self.commands_client.say(most_confident_class)

        self.running = False

    def get_class_of_last_image(self):

        results = self.object_detector.predict(self.last_image)
        most_confident_class = self.object_detector.get_most_confident_class(results)
        return most_confident_class

    def move_step(self):

        self.commands_client.move_turn_left()
        time.sleep(ComplexCommandRoom.time_sleep_move)
        self.commands_client.move_stop()
        time.sleep(ComplexCommandRoom.time_sleep_adjust_image)



