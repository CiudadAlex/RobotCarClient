from managers.SpeakManager import SpeakManager
from inforeception.CarInformationReceptor import CarInformationReceptor
from textinterpreter.TextCommandInterpreter import TextCommandInterpreter


class Engine:

    text_command_interpreter = None

    @staticmethod
    def start(car_speaks, commands_by_audio, connect_to_video_stream, connect_to_audio_or_text_command_stream):

        SpeakManager.get_instance().car_speaks = car_speaks

        Engine.text_command_interpreter = TextCommandInterpreter()

        CarInformationReceptor.build_instance(commands_by_audio=commands_by_audio,
                                              connect_to_video_stream=connect_to_video_stream,
                                              connect_to_audio_or_text_command_stream=connect_to_audio_or_text_command_stream,
                                              on_text_received=Engine.on_text_received)

    @staticmethod
    def on_text_received(text):
        print(f"############################ {text}")
        Engine.text_command_interpreter.interpret(text)

