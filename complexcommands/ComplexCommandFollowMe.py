from clients.CommandsClient import CommandsClient
from ai.video.Tracker import Tracker
import time


class ComplexCommandFollowMe:

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommandFollowMe.instance is None:
            ComplexCommandFollowMe.instance = ComplexCommandFollowMe()

        return ComplexCommandFollowMe.instance

    def __init__(self):
        self.last_image = None
        self.commands_client = CommandsClient.get_instance()

    def execute(self):
        pass

    # FIXME implement



