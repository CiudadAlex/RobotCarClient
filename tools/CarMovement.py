from clients.CommandsClient import CommandsClient


class CarMovement:

    def __init__(self):
        self.commands_client = CommandsClient.get_instance()

    def move_right(self):
        self.commands_client.move_a_bit_turn_right(0.12)

    def move_left(self):
        self.commands_client.move_a_bit_turn_left(0.12)

    def move_ahead(self):
        self.commands_client.move_a_bit_forward(0.7)
