from remotecontrolui.RemoteControlUI import RemoteControlUI
from engine.Engine import Engine


online = True


if __name__ == "__main__":
    Engine.start(car_speaks=False,
                 connect_to_video_stream=online,
                 connect_to_audio_stream=online,
                 connect_to_text_stream=online)

    RemoteControlUI.launch()


# FIXME Test Edge recognition to guide.


# FIXME Wall follower
# FIXME Room recognizer: redo training with higher look


# FIXME ComplexCommandGoToRoom (Door recognition model)


# FIXME revise espeak (makes 360 hang)
