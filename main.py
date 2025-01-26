from remotecontrolui.RemoteControlUI import RemoteControlUI
from engine.Engine import Engine


online = True


if __name__ == "__main__":
    Engine.start(car_speaks=True,
                 connect_to_video_stream=online,
                 connect_to_audio_stream=online,
                 connect_to_text_stream=online)

    RemoteControlUI.launch()


# FIXME test: Speakers to answer
# FIXME test: in follow me look both sides before complete turn around
# FIXME test: LLM with contexts
# FIXME test: room sum probabilities
# FIXME test: generate corpus with val and test images

# FIXME revise Command 360 does not work properly through webUI
# FIXME revise espeak


# FIXME Room recognizer: redo training with higher look
# FIXME ComplexCommandGoToRoom (Door recognition model)



