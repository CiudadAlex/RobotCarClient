from clients.AbstractStreamClient import AbstractStreamClient


class TextStreamClient(AbstractStreamClient):

    def __init__(self, host, port, on_text_received):
        super().__init__(host, port)
        self.on_text_received = on_text_received

    def use_item_metadata_and_bytes(self, item_metadata, item_bytes):

        decoded_string = item_bytes.decode("utf-8")
        self.on_text_received(decoded_string)

