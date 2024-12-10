import requests
from utils.PropertiesReader import PropertiesReader
from threading import Thread
import queue


class CommandsClient(Thread):

    instance = None

    @staticmethod
    def get_instance():

        if CommandsClient.instance is None:
            CommandsClient.instance = CommandsClient.build_instance()
            CommandsClient.instance.start()

        return CommandsClient.instance

    @staticmethod
    def build_instance():
        properties_reader = PropertiesReader.get_instance()
        host = properties_reader.host
        port_commands_rest_api = int(properties_reader.port_commands_rest_api)
        return CommandsClient(host, port_commands_rest_api)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.queue_of_command_paths = queue.Queue()

    def run(self):

        while True:
            command_path = self.queue_of_command_paths.get()
            self.execute_command_path(command_path)
            self.queue_of_command_paths.task_done()

    def execute_command_path(self, command_path):
        print(f'Command : {command_path}')
        response = requests.post(f'http://{self.host}:{self.port}/{command_path}')
        print(f'Response: {response.status_code}')

    def led(self, mode):

        command_path = f'led/{mode}'
        self.queue_of_command_paths.put(command_path)

    def move(self, mode):

        command_path = f'move/{mode}'
        self.queue_of_command_paths.put(command_path)

    def look(self, mode):

        command_path = f'look/{mode}'
        self.queue_of_command_paths.put(command_path)

    def look_up(self):
        self.look("up")

    def look_down(self):
        self.look("down")

    def look_home(self):
        self.look("home")

    def listen(self, mode):

        command_path = f'listen/{mode}'
        self.queue_of_command_paths.put(command_path)

    def listen_on(self):
        self.listen("on")

    def listen_off(self):
        self.listen("off")

