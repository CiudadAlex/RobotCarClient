import threading
from tools.ImageUtils import ImageUtils
from clients.CommandsClient import CommandsClient
from inforeception.CarInformationReceptor import CarInformationReceptor


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
        self.commands_client = CommandsClient.get_instance()

        CarInformationReceptor.get_instance().list_on_image_received.append(self.set_last_image)

    def set_last_image(self, image):
        if self.recording:
            self.list_image.append(image)

    def switch_recording(self):

        if self.recording:
            self.set_recording_off()
        else:
            self.set_recording_on()

    def set_recording_on(self):
        self.recording = True
        self.commands_client.led_red()

    def set_recording_off(self):
        self.recording = False
        self.commands_client.led_fading_red()

        if len(self.list_image) > 0:
            self.create_video_in_thread()

    def create_video_in_thread(self):

        create_video_thread = threading.Thread(target=self.create_video)
        create_video_thread.start()

    def create_video(self):
        self.video_id = self.video_id + 1
        ImageUtils.generate_mp4(f"{self.path_output}/video_{self.video_id}.mp4", self.list_image, fps=10)
        self.list_image = []
