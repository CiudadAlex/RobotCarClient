from clients.CommandsClient import CommandsClient
import time


class ComplexCommand360:

    @staticmethod
    def execute():
        commands_client = CommandsClient.get_instance()
        commands_client.move_turn_left()
        time.sleep(0.3)
        commands_client.move_stop()

        # FIXME implement

