from remotecontrolui.RemoteControlUI import RemoteControlUI
from managers.SpeakManager import SpeakManager


if __name__ == "__main__":
    SpeakManager.get_instance().car_speaks = False
    RemoteControlUI.launch(connect_to_video_stream=True,
                           connect_to_audio_or_text_command_stream=True)


# FIXME test: follow me look to the side to find person
# FIXME test: emergency brake (Stop only if going forward)
# FIXME test: stop for Command Follow me
# FIXME test: Speakers to answer
# FIXME test: Room recognizer


# FIXME Room recognizer: More photographs if doubt
# FIXME Refactor to constant: room_s_2024_12_28 + DetermineRoomHelper

# FIXME Door recognizer
# FIXME LLM with contexts
# FIXME Command: Go to room (use RoomRouter)



