import time

from clients.ImageStreamClient import ImageStreamClient


def on_image_received(image):
    # image.show()
    pass


if __name__ == "__main__":
    imageStreamClient = ImageStreamClient('192.168.0.19', 8000, on_image_received)

    time.sleep(30)


# FIXME host and port in properties
# FIXME UI to see the videostream

