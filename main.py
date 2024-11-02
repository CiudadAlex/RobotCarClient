from remotecontrolui.RemoteControlUI import RemoteControlUI
from utils.PropertiesReader import PropertiesReader
from clients.TextStreamClient import TextStreamClient
from clients.AudioStreamClient import AudioStreamClient


commands_by_audio = True


def on_text_received(text):
    print(f"############################ {text}")


if __name__ == "__main__":

    # RemoteControlUI.launch()

    properties_reader = PropertiesReader('config.properties')
    host = properties_reader.host
    port_images_stream = int(properties_reader.port_images_stream)
    port_text_stream = int(properties_reader.port_text_stream)
    port_audio_stream = int(properties_reader.port_audio_stream)

    if commands_by_audio:
        audio_stream_client = AudioStreamClient(host, port_audio_stream, on_text_received)
        audio_stream_client.start()
    else:
        text_stream_client = TextStreamClient(host, port_text_stream, on_text_received)
        text_stream_client.start()


# FIXME CommandsClient
