from clients.CommandsClient import CommandsClient
import time


class CarMovement:

    def __init__(self):
        self.commands_client = CommandsClient.get_instance()

    def move_right(self):
        self.commands_client.move_turn_right()
        time.sleep(0.12)
        self.commands_client.move_stop()

    def move_left(self):
        self.commands_client.move_turn_left()
        time.sleep(0.12)
        self.commands_client.move_stop()

    def move_ahead(self):
        self.commands_client.move_forward()
        time.sleep(0.7)
        self.commands_client.move_stop()
