from clients.CommandsClient import CommandsClient
from tools.Text2SpeechEngine import Text2SpeechEngine


class SpeakManager:

    instance = None

    @staticmethod
    def get_instance():
        if SpeakManager.instance is None:
            SpeakManager.instance = SpeakManager()

        return SpeakManager.instance

    def __init__(self):
        self.car_speaks = False
        self.commands_client = CommandsClient.get_instance()
        self.text_2_speech_engine = Text2SpeechEngine("en")

    def say(self, text_raw):

        self.commands_client.listen_off()
        print(f"listen = off")

        text = "3 2 1: " + text_raw
        print(f"say = {text}")
        if self.car_speaks:
            self.commands_client.say(text)
        else:
            self.text_2_speech_engine.say(text)

        self.commands_client.listen_on()
        print(f"listen = on")


