from clients.CommandsClient import CommandsClient
from utils.PropertiesReader import PropertiesReader
from textinterpreter.music.MusicPlayer import MusicPlayer


class TextCommandInterpreter:

    MODE_COMMAND = "MODE_COMMAND"
    MODE_MUSIC = "MODE_MUSIC"
    MODE_QUESTIONS = "MODE_QUESTIONS"

    commands_change_mode = {
                        MODE_COMMAND: ["change command"],
                        MODE_MUSIC: ["change music"],
                        MODE_QUESTIONS: ["change questions", "change question"]
                        }

    commands_complex = {
                        "follow me": ["follow me"],
                        "360": ["360", "3 60", "three sixty", "tree 60"],
                        "record": ["record"],
                        "go to room": ["go to room"]
                        }
    commands_led = {
                    "police": ["police"],
                    "stop": ["stop"],
                    "alarm": ["alarm"],
                    "rainbow": ["rainbow"],
                    "rainbow flag": ["rainbow flag"],
                    "breathe": ["breathe"]
                    }

    def __init__(self):
        self.commands_client = CommandsClient.get_instance()
        self.mode = TextCommandInterpreter.MODE_COMMAND
        self.properties_reader = PropertiesReader.get_instance()
        self.music_player = MusicPlayer(self.properties_reader.music_dir_path, self.properties_reader.vlc_executable_path)

    def interpret(self, text):

        text = text.lower()

        interpreted = self.interpret_change_mode(text)

        if interpreted:
            return

        print(f"No interpretation of: {text}")

    def interpret_change_mode(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_complex, "CHANGE MODE", self.execute_change_mode)

    def interpret_command_complex(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_complex, "COMPLEX", self.execute_complex_command)

    def interpret_command_led(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_led, "LED", self.commands_client.led)

    @staticmethod
    def interpret_command(text, map_command_utterances, command_type, func):

        for comm, list_utterances in map_command_utterances.items():

            for utterance in list_utterances:
                if utterance in text:
                    print(f"{command_type} command: {comm}")
                    func(comm)
                    return True

        return False

    def execute_change_mode(self, text):
        self.mode = text

    def execute_complex_command(self, text):
        print(f">>>>>>>>>>>>>>>>>>>>> COMPLEX_COMMAND = {text}")

# FIXME MusicPlayer

