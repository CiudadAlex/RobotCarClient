from clients.CommandsClient import CommandsClient


class TextCommandInterpreter:

    complex_commands = ["follow me", "360", "record", "go to room"]
    led_commands = ["police", "stop", "alarm", "rainbow", "rainbow flag", "breathe"]

    def __init__(self):
        self.commands_client = CommandsClient.get_instance()

    def interpret(self, text):

        for comm in TextCommandInterpreter.led_commands:
            if comm in text:
                print(f"LED command: {comm}")
                self.commands_client.led(comm)
                return

        print(f"No interpretation of: {text}")

# FIXME MusicPlayer

