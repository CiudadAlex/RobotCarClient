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
            command_path, body = self.queue_of_command_paths.get()
            self.execute_command_path(command_path, body)
            self.queue_of_command_paths.task_done()

    def execute_command_path(self, command_path, body):
        print(f'Command : {command_path}')
        response = requests.post(f'http://{self.host}:{self.port}/{command_path}', json=body)
        print(f'Response: {response.status_code}')

    def led(self, mode):

        command_path = f'led/{mode}'
        self.queue_of_command_paths.put((command_path, None))

    def led_stop(self):
        self.led("stop")

    def led_alarm(self):
        self.led("alarm")

    def led_police(self):
        self.led("police")

    def led_rainbow_flag(self):
        self.led("rainbow_flag")

    def led_breathe(self):
        self.led("breathe")

    def led_red(self):
        self.led("red")

    def led_fading_red(self):
        self.led("fading_red")

    def move(self, mode):

        command_path = f'move/{mode}'
        self.queue_of_command_paths.put((command_path, None))

    def move_forward(self):
        self.move("forward")

    def move_backward(self):
        self.move("backward")

    def move_turn_left(self):
        self.move("turn_left")

    def move_turn_right(self):
        self.move("turn_right")

    def move_stop(self):
        self.move("stop")

    def look(self, mode):

        command_path = f'look/{mode}'
        self.queue_of_command_paths.put((command_path, None))

    def look_up(self):
        self.look("up")

    def look_down(self):
        self.look("down")

    def look_home(self):
        self.look("home")

    def listen(self, mode):

        command_path = f'listen/{mode}'
        self.queue_of_command_paths.put((command_path, None))

    def listen_on(self):
        self.listen("on")

    def listen_off(self):
        self.listen("off")

    def say(self, text):

        command_path = 'say'
        self.queue_of_command_paths.put((command_path, text))

