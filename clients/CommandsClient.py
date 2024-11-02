import requests


class CommandsClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def led(self, mode):
        response = requests.post(f'http://{self.host}:{self.port}/led/{mode}')
        print(f'Response: {response.status_code}')

