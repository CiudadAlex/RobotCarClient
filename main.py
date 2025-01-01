from remotecontrolui.RemoteControlUI import RemoteControlUI
from engine.Engine import Engine


online = True


if __name__ == "__main__":
    Engine.start(car_speaks=False,
                 commands_by_audio=True,
                 connect_to_video_stream=online,
                 connect_to_audio_or_text_command_stream=online)

    RemoteControlUI.launch()


# FIXME test: selector of room and door in UI Web
# FIXME Room recognizer: More photographs if doubt

# FIXME follow me: look both sides before complete turn around
# FIXME ComplexCommandGoToRoom (Door recognition model)


# FIXME Speakers to answer
# FIXME LLM with contexts

