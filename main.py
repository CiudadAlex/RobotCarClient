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
# FIXME test: Speakers to answer
# FIXME test: in follow me look both sides before complete turn around
# FIXME test: LLM with contexts

# FIXME Text server to transmit Client commands


# FIXME Room recognizer: redo training with higher look
# FIXME ComplexCommandGoToRoom (Door recognition model)



