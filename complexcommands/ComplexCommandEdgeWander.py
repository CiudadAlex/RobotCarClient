from inforeception.CarInformationReceptor import CarInformationReceptor
from managers.EdgeNavigatorManager import EdgeNavigatorManager
from clients.CommandsClient import CommandsClient
import threading
import time


class ComplexCommandEdgeWander:

    CLOSE_TO_THE_WALL = 0.2
    SECS_BACKWARD = 0.4

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommandEdgeWander.instance is None:
            ComplexCommandEdgeWander.instance = ComplexCommandEdgeWander()

        return ComplexCommandEdgeWander.instance

    def __init__(self):
        self.running = False
        self.edge_navigator_manager = EdgeNavigatorManager.get_instance()
        self.commands_client = CommandsClient.get_instance()

    def stop(self):
        self.running = False

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandEdgeWander!!!!!!!")

        self.running = True

        while self.running:

            distance = self.commands_client.get_distance_to_obstacle(self)

            if distance < ComplexCommandEdgeWander.CLOSE_TO_THE_WALL:
                self.commands_client.move_a_bit_backward(ComplexCommandEdgeWander.SECS_BACKWARD)
                time.sleep(1.2)
            else:
                last_image = CarInformationReceptor.get_instance().last_image
                self.edge_navigator_manager.navigate(last_image)
                time.sleep(1.2)

