from remotecontrolui.RemoteControlUI import RemoteControlUI


if __name__ == "__main__":

    RemoteControlUI.launch(connect_to_video_stream=True, connect_to_audio_or_text_command_stream=True)


# FIXME test ask LLM
# FIXME test Command: Follow me


# FIXME Generator Corpus Yolo
# FIXME Room recognizer
# FIXME Record Video >> ImageUtils.generate_mp4(f"{path_output}/video_{self.video_id}.mp4", list_images_pil)
# FIXME Speakers to answer


# FIXME Door recognizer
# FIXME LLM with contexts
# FIXME Command: Go to room (use RoomRouter)



