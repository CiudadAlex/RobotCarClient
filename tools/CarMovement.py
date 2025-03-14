from clients.CommandsClient import CommandsClient


class CarMovement:

    def __init__(self, secs_forward=0.7, secs_turn=0.12):
        self.commands_client = CommandsClient.get_instance()
        self.secs_forward = secs_forward
        self.secs_turn = secs_turn

    def move_right(self):
        self.commands_client.move_a_bit_turn_right(self.secs_turn)

    def move_left(self):
        self.commands_client.move_a_bit_turn_left(self.secs_turn)

    def move_ahead(self):
        self.commands_client.move_a_bit_forward(self.secs_forward)
