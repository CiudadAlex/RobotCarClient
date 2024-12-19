from clients.CommandsClient import CommandsClient
import time


class ComplexCommand360:

    number_of_steps = 20

    time_sleep_move = 0.3
    time_sleep_adjust_image = 1.5

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommand360.instance is None:
            ComplexCommand360.instance = ComplexCommand360()

        return ComplexCommand360.instance

    def __init__(self):
        self.running = False
        self.last_image = None
        self.selected_room = None
        self.commands_client = CommandsClient.get_instance()

    def execute(self):

        self.running = True

        for step in range(ComplexCommand360.number_of_steps):

            if not self.running:
                return

            self.move_step()
            self.last_image.save(f'.out/image_{step}.png')

            # FIXME generate corpus

    def move_step(self):

        self.commands_client.move_turn_left()
        time.sleep(ComplexCommand360.time_sleep_move)
        self.commands_client.move_stop()
        time.sleep(ComplexCommand360.time_sleep_adjust_image)

