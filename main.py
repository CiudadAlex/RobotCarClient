from remotecontrolui.RemoteControlUI import RemoteControlUI


if __name__ == "__main__":

    RemoteControlUI.launch(connect_to_video_stream=True,
                           connect_to_audio_or_text_command_stream=True,
                           car_speaks=True)


# FIXME test: follow me look to the side to find person
# FIXME test: emergency brake
# FIXME test: stop for Command Follow me
# FIXME test: Speakers to answer

# FIXME Make complex commands a thread (to be able to stop them)
# FIXME Room recognizer


# FIXME Door recognizer
# FIXME LLM with contexts
# FIXME Command: Go to room (use RoomRouter)



