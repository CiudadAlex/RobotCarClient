from clients.CommandsClient import CommandsClient
from utils.PropertiesReader import PropertiesReader
from textinterpreter.music.MusicPlayer import MusicPlayer
from ai.llm.InformationRetriever import InformationRetriever
from tools.Text2SpeechEngine import Text2SpeechEngine
from tools.Wikipedia import Wikipedia


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
        self.information_retriever = InformationRetriever(self.properties_reader.model_llama_ccp_path)
        self.text_2_speech_engine = Text2SpeechEngine("en")
        self.wikipedia = Wikipedia()

    def interpret(self, text):

        text = text.lower()

        interpreted = self.interpret_change_mode(text)

        if interpreted:
            return True

        if self.mode == TextCommandInterpreter.MODE_COMMAND:
            return self.interpret_command(text)
        elif self.mode == TextCommandInterpreter.MODE_MUSIC:
            return self.interpret_music(text)
        elif self.mode == TextCommandInterpreter.MODE_QUESTIONS:
            return self.interpret_questions(text)
        else:
            print(f"Unknown mode: {self.mode}")
            return False

    def interpret_change_mode(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_complex, "CHANGE MODE", self.execute_change_mode)

    def interpret_command(self, text):

        if self.interpret_command_complex(text):
            return True
        elif self.interpret_command_led(text):
            return True
        else:
            print(f"No interpretation of command: {text}")
            return False

    def interpret_command_complex(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_complex, "COMPLEX", self.execute_complex_command)

    def interpret_command_led(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_led, "LED", self.commands_client.led)

    def interpret_music(self, text):
        self.music_player.process_text(text)
        return True

    def interpret_questions(self, text):

        num_of_words = len(text.split())

        if num_of_words > 2:
            answer = self.information_retriever.get_answer(text)
        else:
            answer = self.wikipedia.retrieve_first_part(text)

        print(f"answer = {answer}")
        self.text_2_speech_engine.say(answer)

        return True

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
        # FIXME implement

