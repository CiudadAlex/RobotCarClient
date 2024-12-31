from remotecontrolui.RemoteControlUI import RemoteControlUI
from engine.Engine import Engine


online = True


if __name__ == "__main__":
    Engine.start(car_speaks=False,
                 commands_by_audio=True,
                 connect_to_video_stream=online,
                 connect_to_audio_or_text_command_stream=online)

    RemoteControlUI.launch()


# FIXME test: ComplexCommandPhotoDoor
# FIXME test: ComplexCommandGoToRoom

# FIXME follow me: look both sides before complete turn around
# FIXME Room recognizer: More photographs if doubt
# FIXME selector of room and door in UI Web
# FIXME store in car list of rooms and doors


# FIXME Speakers to answer
# FIXME LLM with contexts




