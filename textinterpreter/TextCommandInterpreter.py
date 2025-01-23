from clients.CommandsClient import CommandsClient
from utils.PropertiesReader import PropertiesReader
from textinterpreter.music.MusicPlayer import MusicPlayer
from ai.llm.InformationRetriever import InformationRetriever
from ai.llm.LLMContexts import LLMContexts
from tools.Wikipedia import Wikipedia
from complexcommands.ComplexCommand360 import ComplexCommand360
from complexcommands.ComplexCommandFollowMe import ComplexCommandFollowMe
from complexcommands.ComplexCommandRecord import ComplexCommandRecord
from complexcommands.ComplexCommandRoom import ComplexCommandRoom
from complexcommands.ComplexCommandGoToRoom import ComplexCommandGoToRoom
from complexcommands.ComplexCommandPhotoDoor import ComplexCommandPhotoDoor
from managers.SpeakManager import SpeakManager
import time


class TextCommandInterpreter:

    MODE_COMMAND = "MODE_COMMAND"
    MODE_MUSIC = "MODE_MUSIC"
    MODE_QUESTIONS = "MODE_QUESTIONS"

    COMPLEX_COMMAND_360 = "COMPLEX_COMMAND_360"
    COMPLEX_COMMAND_FOLLOW_ME = "COMPLEX_COMMAND_FOLLOW_ME"
    COMPLEX_COMMAND_RECORD = "COMPLEX_COMMAND_RECORD"
    COMPLEX_COMMAND_ROOM = "COMPLEX_COMMAND_ROOM"
    COMPLEX_COMMAND_GO_TO_ROOM = "COMPLEX_COMMAND_GO_TO_ROOM"
    COMPLEX_COMMAND_PHOTO_DOOR = "COMPLEX_COMMAND_PHOTO_DOOR"

    commands_change_mode = {
                        MODE_COMMAND: ["change command", "change commands", "command", "commands"],
                        MODE_MUSIC: ["change music", "music"],
                        MODE_QUESTIONS: ["change questions", "change question", "question", "questions"]
                        }

    commands_complex = {
                        COMPLEX_COMMAND_FOLLOW_ME: ["follow me", "follow"],
                        COMPLEX_COMMAND_360: ["360", "3 60", "60", "three sixty", "tree 60"],
                        COMPLEX_COMMAND_RECORD: ["record"],
                        COMPLEX_COMMAND_GO_TO_ROOM: ["go to room", "go room", "go now"],
                        COMPLEX_COMMAND_ROOM: ["room", "where are you", "where"],
                        COMPLEX_COMMAND_PHOTO_DOOR: ["photo", "door"],
                        }
    commands_led = {
                    "police": ["police"],
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
        self.wikipedia = Wikipedia()

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

        if self.interpret_command_stop(text):
            return True
        elif self.interpret_command_complex(text):
            return True
        elif self.interpret_command_led(text):
            return True
        else:
            print(f"No interpretation of command: {text}")
            return False

    def interpret_command_stop(self, text):

        if text == "stop":
            self.stop_all()
            return True

        return False

    def interpret_command_complex(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_complex, "COMPLEX", self.execute_complex_command)

    def interpret_command_led(self, text):
        return self.interpret_command(text, TextCommandInterpreter.commands_led, "LED", self.commands_client.led)

    def interpret_music(self, text):

        self.commands_client.listen_off()
        print(f"listen = off")

        self.music_player.process_text(text)

        self.commands_client.listen_on()
        print(f"listen = on")

        return True

    def interpret_questions(self, text):

        self.commands_client.listen_off()
        print(f"listen = off")

        num_of_words = len(text.split())

        if num_of_words > 2:
            answer = self.information_retriever.get_answer(text, context=LLMContexts.SCHEMATIC)
        else:
            answer = self.wikipedia.retrieve_first_part(text)

        SpeakManager.get_instance().say(answer)

        self.commands_client.listen_on()
        print(f"listen = on")

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

    def execute_change_mode(self, new_mode):
        print(f">>>>>>>>>>>>>>>>>>>>> NEW MODE = {new_mode}")
        SpeakManager.get_instance().say(new_mode.replace("_", " "))
        self.mode = new_mode

        if self.mode == TextCommandInterpreter.MODE_COMMAND:
            self.commands_client.led_stop()
        elif self.mode == TextCommandInterpreter.MODE_MUSIC:
            self.commands_client.led_rainbow_flag()
        elif self.mode == TextCommandInterpreter.MODE_QUESTIONS:
            self.commands_client.led_breathe()
        else:
            self.commands_client.led_stop()

    def stop_all(self, stop_recording=True):

        ComplexCommandFollowMe.get_instance().stop()
        ComplexCommand360.get_instance().stop()
        ComplexCommandRoom.get_instance().stop()
        ComplexCommandGoToRoom.get_instance().stop()
        self.commands_client.led_stop()

        if stop_recording:
            ComplexCommandRecord.get_instance().set_recording_off()

    def execute_complex_command(self, complex_command):
        print(f">>>>>>>>>>>>>>>>>>>>> COMPLEX_COMMAND = {complex_command}")

        if TextCommandInterpreter.COMPLEX_COMMAND_360 == complex_command:

            self.stop_all(stop_recording=False)
            time.sleep(1)
            SpeakManager.get_instance().say("360")
            ComplexCommand360.get_instance().execute()

        elif TextCommandInterpreter.COMPLEX_COMMAND_FOLLOW_ME == complex_command:

            self.stop_all(stop_recording=False)
            time.sleep(1)
            SpeakManager.get_instance().say("Following")
            ComplexCommandFollowMe.get_instance().execute()

        elif TextCommandInterpreter.COMPLEX_COMMAND_ROOM == complex_command:

            self.stop_all(stop_recording=False)
            time.sleep(1)
            SpeakManager.get_instance().say("Room")
            ComplexCommandRoom.get_instance().execute()

        elif TextCommandInterpreter.COMPLEX_COMMAND_GO_TO_ROOM == complex_command:

            self.stop_all(stop_recording=False)
            time.sleep(1)
            SpeakManager.get_instance().say("Go to room")
            ComplexCommandGoToRoom.get_instance().execute()

        elif TextCommandInterpreter.COMPLEX_COMMAND_PHOTO_DOOR == complex_command:

            self.stop_all(stop_recording=False)
            time.sleep(1)
            SpeakManager.get_instance().say("Photo")
            ComplexCommandPhotoDoor.get_instance().execute()

        elif TextCommandInterpreter.COMPLEX_COMMAND_RECORD == complex_command:
            print("Record!!!!!!!")
            SpeakManager.get_instance().say("Record")
            ComplexCommandRecord.get_instance().switch_recording()

        else:
            print(f"No implementation for complex command {complex_command}")

