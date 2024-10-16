import time

from clients.ImageStreamClient import ImageStreamClient


if __name__ == "__main__":
    imageStreamClient = ImageStreamClient('192.168.0.19', 8000)

    time.sleep(30)


# FIXME check image dimensions
# FIXME finish

