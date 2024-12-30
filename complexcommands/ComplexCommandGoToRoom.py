from clients.CommandsClient import CommandsClient
from ai.video.ObjectDetector import ObjectDetector
from tools.RoomRouter import RoomRouter
from inforeception.CarInformationReceptor import CarInformationReceptor
from inforeception.SelectedDataReceptor import SelectedDataReceptor
import threading


class ComplexCommandGoToRoom:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandGoToRoom.instance is None:
            ComplexCommandGoToRoom.instance = ComplexCommandGoToRoom()

        return ComplexCommandGoToRoom.instance

    def __init__(self):
        self.running = False
        self.commands_client = CommandsClient.get_instance()
        self.object_detector = ObjectDetector.load_custom_model("room_s_2024_12_28")
        self.room_router = RoomRouter()

    def stop(self):
        self.running = False

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandGoToRoom!!!!!!!")

        self.running = True

        # FIXME calculate from ComplexCommandRoom (refactor)
        room_start = None
        room_end = SelectedDataReceptor.get_instance().selected_room
        route = self.room_router.create_route(room_start, room_end)

        self.running = False

