from clients.AbstractStreamClient import AbstractStreamClient
from PIL import Image


class ImageStreamClient(AbstractStreamClient):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.count = 0
        self.start()

    def use_item_metadata_and_bytes(self, item_metadata, item_bytes):

        str_item_metadata = item_metadata.decode("utf-8")
        array_metadata = str_item_metadata.split(",")
        width = int(array_metadata[0])
        height = int(array_metadata[1])
        print(f"image size = {width} x {height}")

        image = Image.frombytes('RGBA', (width, height), item_bytes)

        if self.count % 30 == 0:
            image.show()

        self.count = self.count + 1

# FIXME finish

