import socket
import struct
from PIL import Image


def receive_images():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.0.19', 8000))

    while True:
        image_size = struct.unpack('>I', client_socket.recv(4))[0]
        print("image_size = " + str(image_size))
        image_bytes = b""
        while len(image_bytes) < image_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            image_bytes += packet

        image = Image.frombytes('RGBA', (240, 60), image_bytes)
        image.show()


if __name__ == "__main__":
    receive_images()

# FIXME check image dimensions
# FIXME finish

