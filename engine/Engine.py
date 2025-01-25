from managers.SpeakManager import SpeakManager
from inforeception.CarInformationReceptor import CarInformationReceptor
from textinterpreter.TextCommandInterpreter import TextCommandInterpreter
from utils.PropertiesReader import PropertiesReader
from clients.CommandsClient import CommandsClient
from tools.RoomRouter import RoomRouter


class Engine:

    text_command_interpreter = None

    @staticmethod
    def start(car_speaks, connect_to_video_stream, connect_to_audio_stream, connect_to_text_stream):

        SpeakManager.get_instance().car_speaks = car_speaks

        Engine.text_command_interpreter = TextCommandInterpreter()

        Engine.set_room_list_and_door_list_in_car()

        CarInformationReceptor.build_instance(connect_to_video_stream=connect_to_video_stream,
                                              connect_to_audio_stream=connect_to_audio_stream,
                                              connect_to_text_stream=connect_to_text_stream,
                                              on_text_received=Engine.on_text_received)


    @staticmethod
    def set_room_list_and_door_list_in_car():

        properties_reader = PropertiesReader.get_instance()
        commands_client = CommandsClient.get_instance()
        room_router = RoomRouter()

        room_list = properties_reader.room_list
        door_list = ','.join(room_router.get_list_all_adjacency())

        commands_client.set_room_list(room_list)
        commands_client.set_door_list(door_list)

    @staticmethod
    def on_text_received(text):
        print(f"############################ {text}")
        Engine.text_command_interpreter.interpret(text)

