from clients.CommandsClient import CommandsClient
from utils.PropertiesReader import PropertiesReader
from utils.YoloDatasetBuilder import YoloDatasetBuilder
from inforeception.CarInformationReceptor import CarInformationReceptor
from inforeception.SelectedDataReceptor import SelectedDataReceptor
import threading
import time


class ComplexCommand360:

    number_of_steps = 20

    time_sleep_move = 0.15
    time_sleep_adjust_image = 1.5

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommand360.instance is None:
            ComplexCommand360.instance = ComplexCommand360()

        return ComplexCommand360.instance

    def __init__(self):
        self.running = False
        self.commands_client = CommandsClient.get_instance()

        properties_reader = PropertiesReader.get_instance()
        room_dataset_path = properties_reader.room_dataset_path
        room_list = properties_reader.room_list.split(",")
        self.yolo_dataset_builder = YoloDatasetBuilder(room_dataset_path, room_list)
        self.yolo_dataset_builder.build_structure()

    def stop(self):
        self.running = False

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommand360!!!!!!!")

        self.running = True

        room_json = SelectedDataReceptor.get_instance().get_room()
        selected_room_id = room_json["selected_room_id"]
        selected_room_name = room_json["selected_room_name"]

        for step in range(ComplexCommand360.number_of_steps):

            if not self.running:
                return

            self.move_step()
            self.save_image_in_corpus(selected_room_id, selected_room_name)

    def save_image_in_corpus(self, selected_room_id, selected_room_name):

        if selected_room_id is None:
            print("No selected ROOM")
            return

        last_image = CarInformationReceptor.get_instance().last_image
        self.yolo_dataset_builder.save_image_in_corpus(last_image, selected_room_id, selected_room_name)

    def move_step(self):

        self.commands_client.move_turn_left()
        time.sleep(ComplexCommand360.time_sleep_move)
        self.commands_client.move_stop()
        time.sleep(ComplexCommand360.time_sleep_adjust_image)

