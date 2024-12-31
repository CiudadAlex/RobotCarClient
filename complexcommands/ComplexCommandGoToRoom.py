from tools.RoomRouter import RoomRouter
from clients.CommandsClient import CommandsClient
from complexcommands.helpers.DetermineRoomHelper import DetermineRoomHelper
from inforeception.SelectedDataReceptor import SelectedDataReceptor
from ai.video.ObjectDetector import ObjectDetector
from inforeception.CarInformationReceptor import CarInformationReceptor
from ai.video.Models import Models
import threading
import time


class ComplexCommandGoToRoom:

    time_sleep_move_turn = 0.1
    time_sleep_move_forward = 2
    time_sleep_adjust_image = 1.5

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandGoToRoom.instance is None:
            ComplexCommandGoToRoom.instance = ComplexCommandGoToRoom()

        return ComplexCommandGoToRoom.instance

    def __init__(self):
        self.running = False
        self.determine_room_helper = DetermineRoomHelper()
        self.room_router = RoomRouter()
        self.commands_client = CommandsClient.get_instance()
        self.object_detector = ObjectDetector.load_custom_model(Models.MODEL_DOOR_DETECTION)

    def stop(self):
        self.running = False
        self.determine_room_helper.stop()

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandGoToRoom!!!!!!!")

        room_json = SelectedDataReceptor.get_instance().get_room()
        room_end = room_json.selected_room_name

        self.running = True

        room_start = self.determine_room_helper.get_room()

        route = self.room_router.create_route(room_start, room_end)

        if len(route) == 0:
            self.running = False
            return

        next_room = route[0]

        self.find_door()

        self.running = False

    def find_door(self):

        while self.running:

            last_image = CarInformationReceptor.get_instance().last_image
            results = self.object_detector.predict(last_image)

            if results is None:
                self.move_step()
                continue

            list_class_and_confidence = self.object_detector.get_list_class_and_confidence(results)

            if len(list_class_and_confidence) == 0:
                self.move_step()
                continue

            self.commands_client.move_forward()
            time.sleep(ComplexCommandGoToRoom.time_sleep_move_forward)
            self.commands_client.move_stop()
            time.sleep(ComplexCommandGoToRoom.time_sleep_adjust_image)

    def move_step(self):

        self.commands_client.move_turn_left()
        time.sleep(ComplexCommandGoToRoom.time_sleep_move_turn)
        self.commands_client.move_stop()
        time.sleep(ComplexCommandGoToRoom.time_sleep_adjust_image)
