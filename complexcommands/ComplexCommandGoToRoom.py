from tools.RoomRouter import RoomRouter
from complexcommands.helpers.DetermineRoomHelper import DetermineRoomHelper
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
        self.determine_room_helper = DetermineRoomHelper()
        self.room_router = RoomRouter()

    def stop(self):
        self.running = False
        self.determine_room_helper.stop()

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandGoToRoom!!!!!!!")

        self.running = True

        room_start = self.determine_room_helper.get_room()
        room_end = SelectedDataReceptor.get_instance().selected_room_name
        route = self.room_router.create_route(room_start, room_end)

        # FIXME finish (find door)

        self.running = False

