from managers.SpeakManager import SpeakManager
from complexcommands.helpers.DetermineRoomHelper import DetermineRoomHelper
import threading


class ComplexCommandRoom:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandRoom.instance is None:
            ComplexCommandRoom.instance = ComplexCommandRoom()

        return ComplexCommandRoom.instance

    def __init__(self):
        self.determine_room_helper = DetermineRoomHelper()

    def stop(self):
        self.determine_room_helper.stop()

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandRoom!!!!!!!")

        room = self.determine_room_helper.get_room()
        SpeakManager.get_instance().say(f"I am in the room {room}")

