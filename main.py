from remotecontrolui.RemoteControlUI import RemoteControlUI
from engine.Engine import Engine


online = True


if __name__ == "__main__":
    Engine.start(car_speaks=False,
                 commands_by_audio=True,
                 connect_to_video_stream=online,
                 connect_to_audio_or_text_command_stream=online)

    RemoteControlUI.launch()


# FIXME test: follow me look to the side to find person
# FIXME test: Speakers to answer

# FIXME Room recognizer: More photographs if doubt
# FIXME Limit of 4 secs to send audio to speech recognition
# FIXME Door recognizer


# FIXME selection of room and door in car
# FIXME LLM with contexts
# FIXME Command: Go to room



