import requests
from utils.PropertiesReader import PropertiesReader


class CommandsClient:

    instance = None

    @staticmethod
    def get_instance():

        if CommandsClient.instance is None:
            CommandsClient.instance = CommandsClient.build_instance()

        return CommandsClient.instance

    @staticmethod
    def build_instance():
        properties_reader = PropertiesReader('config.properties')
        host = properties_reader.host
        port_commands_rest_api = int(properties_reader.port_commands_rest_api)
        return CommandsClient(host, port_commands_rest_api)

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def led(self, mode):
        print(f'Command LED : {mode}')
        response = requests.post(f'http://{self.host}:{self.port}/led/{mode}')
        print(f'Response: {response.status_code}')

