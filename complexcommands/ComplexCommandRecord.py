import threading
from tools.ImageUtils import ImageUtils


class ComplexCommandRecord:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandRecord.instance is None:
            ComplexCommandRecord.instance = ComplexCommandRecord()

        return ComplexCommandRecord.instance

    def __init__(self):
        self.recording = False
        self.list_image = []
        self.video_id = 0
        self.path_output = "./.out"

    def set_last_image(self, image):
        if self.recording:
            self.list_image.append(image)

    def set_recording(self, recording):
        self.recording = recording

        if not self.recording and len(self.list_image) > 0:
            self.create_video_in_thread()

    def create_video_in_thread(self):

        create_video_thread = threading.Thread(target=self.create_video)
        create_video_thread.start()

    def create_video(self):
        self.video_id = self.video_id + 1
        ImageUtils.generate_mp4(f"{self.path_output}/video_{self.video_id}.mp4", self.list_image)
        self.list_image = []
