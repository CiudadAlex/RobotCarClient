from remotecontrolui.RemoteControlUI import RemoteControlUI
from utils.PropertiesReader import PropertiesReader
from clients.TextStreamClient import TextStreamClient
from clients.AudioStreamClient import AudioStreamClient


commands_by_audio = False


def on_text_received(text):
    print(f"######## {text}")


if __name__ == "__main__":

    RemoteControlUI.launch()

    properties_reader = PropertiesReader('config.properties')
    host = properties_reader.host
    port_images_stream = int(properties_reader.port_images_stream)

    if commands_by_audio:
        audio_stream_client = AudioStreamClient(host, port_images_stream, on_text_received)
        audio_stream_client.start()
    else:
        text_stream_client = TextStreamClient(host, port_images_stream, on_text_received)
        text_stream_client.start()


# FIXME TextStreamClient
# FIXME AudioStreamClient

