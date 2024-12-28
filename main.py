from remotecontrolui.RemoteControlUI import RemoteControlUI
from managers.SpeakManager import SpeakManager


if __name__ == "__main__":
    SpeakManager.get_instance().car_speaks = True
    RemoteControlUI.launch(connect_to_video_stream=True,
                           connect_to_audio_or_text_command_stream=True,
                           car_speaks=True)


# FIXME test: follow me look to the side to find person
# FIXME test: emergency brake
# FIXME test: stop for Command Follow me
# FIXME test: Speakers to answer
# FIXME test: Room recognizer

# FIXME Make complex commands a thread (to be able to stop them)
# FIXME Refactor 'say'


# FIXME Door recognizer
# FIXME LLM with contexts
# FIXME Command: Go to room (use RoomRouter)



