from inforeception.SelectedDataReceptor import SelectedDataReceptor
from inforeception.CarInformationReceptor import CarInformationReceptor
from utils.PropertiesReader import PropertiesReader
from utils.YoloDatasetBuilder import YoloDatasetBuilder
from tools.RoomRouter import RoomRouter
import threading


class ComplexCommandPhotoDoor:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandPhotoDoor.instance is None:
            ComplexCommandPhotoDoor.instance = ComplexCommandPhotoDoor()

        return ComplexCommandPhotoDoor.instance

    def __init__(self):

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
        self.save_image_in_corpus()

    def save_image_in_corpus(self):

        selected_door_id = SelectedDataReceptor.get_instance().selected_door_id
        selected_door_name = SelectedDataReceptor.get_instance().selected_door_name

        if selected_door_id is None:
            print("No selected DOOR")
            return

        last_image = CarInformationReceptor.get_instance().last_image
        self.yolo_dataset_builder.save_image_in_corpus(last_image, selected_door_id, selected_door_name)

