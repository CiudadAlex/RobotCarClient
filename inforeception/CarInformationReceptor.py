from clients.TextStreamClient import TextStreamClient
from clients.AudioStreamClient import AudioStreamClient
from clients.ImageStreamClient import ImageStreamClient
from utils.PropertiesReader import PropertiesReader
from textinterpreter.TextCommandInterpreter import TextCommandInterpreter


class CarInformationReceptor:

    instance = None

    @staticmethod
    def get_instance():
        return CarInformationReceptor.instance

    @staticmethod
    def build_instance(commands_by_audio, connect_to_video_stream, connect_to_audio_or_text_command_stream,
                       on_image_received, on_text_received):
        CarInformationReceptor.instance = CarInformationReceptor(commands_by_audio, connect_to_video_stream,
                                                                 connect_to_audio_or_text_command_stream,
                                                                 on_image_received, on_text_received)

    def __init__(self, commands_by_audio, connect_to_video_stream, connect_to_audio_or_text_command_stream,
                 on_image_received):

        self.last_image = None
        self.on_image_received = on_image_received

        self.text_command_interpreter = TextCommandInterpreter()

        self.properties_reader = PropertiesReader.get_instance()
        host = self.properties_reader.host
        port_images_stream = int(self.properties_reader.port_images_stream)
        port_text_stream = int(self.properties_reader.port_text_stream)
        port_audio_stream = int(self.properties_reader.port_audio_stream)

        if connect_to_video_stream:
            image_stream_client = ImageStreamClient(host, port_images_stream, self.on_image_received_action)
            image_stream_client.start()

        if connect_to_audio_or_text_command_stream:
            if commands_by_audio:
                audio_stream_client = AudioStreamClient(host, port_audio_stream, self.on_text_received)
                audio_stream_client.start()
            else:
                text_stream_client = TextStreamClient(host, port_text_stream, self.on_text_received)
                text_stream_client.start()

    def on_text_received(self, text):
        print(f"############################ {text}")
        self.text_command_interpreter.interpret(text)

    def on_image_received_action(self, image):

        self.last_image = image

        if self.on_image_received is not None:
            self.on_image_received(image)
