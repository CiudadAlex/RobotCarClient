import time
from utils.PropertiesReader import PropertiesReader
from clients.ImageStreamClient import ImageStreamClient


def on_image_received(image):
    # image.show()
    pass


if __name__ == "__main__":

    propertiesReader = PropertiesReader('config.properties')
    host = propertiesReader.host
    port_images_stream = propertiesReader.port_images_stream

    imageStreamClient = ImageStreamClient(host, port_images_stream, on_image_received)

    time.sleep(300)


# FIXME test host and port in properties
# FIXME UI to see the videostream

