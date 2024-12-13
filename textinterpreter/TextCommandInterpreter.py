import time

from clients.CommandsClient import CommandsClient
from utils.PropertiesReader import PropertiesReader
from textinterpreter.music.MusicPlayer import MusicPlayer
from ai.llm.InformationRetriever import InformationRetriever
from tools.Text2SpeechEngine import Text2SpeechEngine
from tools.Wikipedia import Wikipedia
from complexcommands.ComplexCommand360 import ComplexCommand360
from complexcommands.ComplexCommandFollowMe import ComplexCommandFollowMe
from complexcommands.ComplexCommandRecord import ComplexCommandRecord


class TextCommandInterpreter:

    MODE_COMMAND = "MODE_COMMAND"
    MODE_MUSIC = "MODE_MUSIC"
    MODE_QUESTIONS = "MODE_QUESTIONS"

    COMPLEX_COMMAND_360 = "COMPLEX_COMMAND_360"
    COMPLEX_COMMAND_FOLLOW_ME = "COMPLEX_COMMAND_FOLLOW_ME"
    COMPLEX_COMMAND_RECORD = "COMPLEX_COMMAND_RECORD"
    COMPLEX_COMMAND_GO_TO_ROOM = "COMPLEX_COMMAND_GO_TO_ROOM"

    commands_change_mode = {
                        MODE_COMMAND: ["change command", "change commands", "command", "commands"],
                        MODE_MUSIC: ["change music", "music"],
                        MODE_QUESTIONS: ["change questions", "change question", "question", "questions"]
                        }

    commands_complex = {
                        COMPLEX_COMMAND_FOLLOW_ME: ["follow me"],
                        COMPLEX_COMMAND_360: ["360", "3 60", "three sixty", "tree 60"],
                        COMPLEX_COMMAND_RECORD: ["record"],
                        COMPLEX_COMMAND_GO_TO_ROOM: ["go to room"]
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
        self.car_speaks = True

    def interpret(self, text):

        text = text.lower()

        interpreted = self.interpret_change_mode(text)

        if interpreted:
            return True

        if self.mode == TextCommandInterpreter.MODE_COMMAND:
            return self.interpret_car_command(text)
        elif self.mode == TextCommandInterpreter.MODE_MUSIC:
            return self.interpret_music(text)
        elif self.mode == TextCommandInterpreter.MODE_QUESTIONS:
            return self.interpret_questions(text)
        else:
            print(f"Unknown mode: {self.mode}")
            return False

    def interpret_change_mode(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_change_mode, "CHANGE MODE", self.execute_change_mode)

    def interpret_car_command(self, text):

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
        self.wrap_func_call_with_listen_off(self.music_player.process_text, text)
        return True

    def interpret_questions(self, text):

        num_of_words = len(text.split())

        if num_of_words > 2:
            answer = self.information_retriever.get_answer(text)
        else:
            answer = self.wikipedia.retrieve_first_part(text)

        print(f"answer = {answer}")
        if self.car_speaks:
            self.commands_client.say(answer)
        else:
            self.wrap_func_call_with_listen_off(self.text_2_speech_engine.say, answer)

        return True

    def wrap_func_call_with_listen_off(self, func, argument):

        self.commands_client.listen_off()
        print(f"listen = off")

        func(argument)

        self.commands_client.listen_on()
        print(f"listen = on")

    @staticmethod
    def interpret_command(text, map_command_utterances, command_type, func):

        for comm, list_utterances in map_command_utterances.items():

            for utterance in list_utterances:
                if utterance in text:
                    print(f"{command_type} command: {comm}")
                    func(comm)
                    return True

        return False

    def execute_change_mode(self, new_mode):
        print(f">>>>>>>>>>>>>>>>>>>>> NEW MODE = {new_mode}")
        self.mode = new_mode

        if self.mode == TextCommandInterpreter.MODE_COMMAND:
            self.commands_client.led_stop()
        elif self.mode == TextCommandInterpreter.MODE_MUSIC:
            self.commands_client.led_rainbow_flag()
        elif self.mode == TextCommandInterpreter.MODE_QUESTIONS:
            self.commands_client.led_breathe()
        else:
            self.commands_client.led_stop()

    def execute_complex_command(self, complex_command):
        print(f">>>>>>>>>>>>>>>>>>>>> COMPLEX_COMMAND = {complex_command}")

        if TextCommandInterpreter.COMPLEX_COMMAND_360 == complex_command:
            print("360!!!!!!!")
            ComplexCommandFollowMe.get_instance().running = False
            time.sleep(1)
            ComplexCommand360.get_instance().execute()

        elif TextCommandInterpreter.COMPLEX_COMMAND_FOLLOW_ME == complex_command:
            print("Follow me!!!!!!!")
            ComplexCommand360.get_instance().running = False
            time.sleep(1)
            ComplexCommandFollowMe.get_instance().execute()

        elif TextCommandInterpreter.COMPLEX_COMMAND_RECORD == complex_command:
            print("Record!!!!!!!")
            ComplexCommandRecord.get_instance().set_recording(True)
            # FIXME switch it off

        else:
            print(f"No implementation for complex command {complex_command}")

        # FIXME implement

