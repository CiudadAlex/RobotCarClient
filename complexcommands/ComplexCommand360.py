from clients.CommandsClient import CommandsClient
import time


class ComplexCommand360:

    last_image = None
    number_of_steps = 10

    time_sleep_move = 0.3
    time_sleep_adjust_image = 1

    @staticmethod
    def execute():

        commands_client = CommandsClient.get_instance()

        for step in range(ComplexCommand360.number_of_steps):
            ComplexCommand360.move_step(commands_client)
            ComplexCommand360.last_image.save(f'.out/image_{step}.png')


    @staticmethod
    def move_step(commands_client):

        commands_client.move_turn_left()
        time.sleep(ComplexCommand360.time_sleep_move)
        commands_client.move_stop()
        time.sleep(ComplexCommand360.time_sleep_adjust_image)

