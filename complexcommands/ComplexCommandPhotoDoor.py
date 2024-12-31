from inforeception.SelectedDataReceptor import SelectedDataReceptor
from inforeception.CarInformationReceptor import CarInformationReceptor
from utils.PropertiesReader import PropertiesReader
from utils.YoloDatasetBuilder import YoloDatasetBuilder
from tools.RoomRouter import RoomRouter
from clients.CommandsClient import CommandsClient
import threading
import time


class ComplexCommandPhotoDoor:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandPhotoDoor.instance is None:
            ComplexCommandPhotoDoor.instance = ComplexCommandPhotoDoor()

        return ComplexCommandPhotoDoor.instance

    def __init__(self):

        self.commands_client = CommandsClient.get_instance()
        properties_reader = PropertiesReader.get_instance()
        door_dataset_path = properties_reader.door_dataset_path
        room_router = RoomRouter()
        door_list = room_router.get_list_all_adjacency()
        self.yolo_dataset_builder = YoloDatasetBuilder(door_dataset_path, door_list)
        self.yolo_dataset_builder.build_structure()

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandPhotoDoor!!!!!!!")
        self.commands_client.led_red()
        self.save_image_in_corpus()
        time.sleep(1)
        self.commands_client.led_stop()

    def save_image_in_corpus(self):

        door_json = SelectedDataReceptor.get_instance().get_door()
        selected_door_id = door_json['selected_door_id']
        selected_door_name = door_json['selected_door_name']

        if selected_door_id is None:
            print("No selected DOOR")
            return

        last_image = CarInformationReceptor.get_instance().last_image
        self.yolo_dataset_builder.save_image_in_corpus(last_image, selected_door_id, selected_door_name)

