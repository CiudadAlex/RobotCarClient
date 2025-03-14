from inforeception.CarInformationReceptor import CarInformationReceptor
from managers.EdgeNavigatorManager import EdgeNavigatorManager
import threading
import time


class ComplexCommandEdgeWander:

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommandEdgeWander.instance is None:
            ComplexCommandEdgeWander.instance = ComplexCommandEdgeWander()

        return ComplexCommandEdgeWander.instance

    def __init__(self):
        self.running = False
        self.edge_navigator_manager = EdgeNavigatorManager.get_instance()

    def stop(self):
        self.running = False

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandEdgeWander!!!!!!!")

        self.running = True

        while self.running:

            last_image = CarInformationReceptor.get_instance().last_image
            self.edge_navigator_manager.navigate(last_image)
            time.sleep(1.2)

