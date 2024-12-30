from remotecontrolui.RemoteControlUI import RemoteControlUI
from managers.SpeakManager import SpeakManager
from inforeception.CarInformationReceptor import CarInformationReceptor


if __name__ == "__main__":
    SpeakManager.get_instance().car_speaks = False
    CarInformationReceptor.build_instance(commands_by_audio=True, connect_to_video_stream=True,
                                          connect_to_audio_or_text_command_stream=True)
    RemoteControlUI.launch()


# FIXME test: follow me look to the side to find person
# FIXME test: emergency brake (Stop only if going forward)
# FIXME test: stop for Command Follow me
# FIXME test: Speakers to answer
# FIXME test: Room recognizer


# FIXME Room recognizer: More photographs if doubt


# FIXME Door recognizer
# FIXME LLM with contexts
# FIXME Command: Go to room (use RoomRouter)



