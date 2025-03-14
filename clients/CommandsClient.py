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
            self.execute_command_path_post(command_path, body)
            self.queue_of_command_paths.task_done()

    def execute_command_path_post(self, command_path, body):
        print(f'Command POST: {command_path}')
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(f'http://{self.host}:{self.port}/{command_path}', json=body, headers=headers)
        print(f'Response POST: {response.status_code}')

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

    def move_a_bit(self, mode, secs):

        command_path = f'move_a_bit/{mode}/{secs}'
        self.queue_of_command_paths.put((command_path, None))

    def move_a_bit_forward(self, secs):
        self.move_a_bit("forward", secs)

    def move_a_bit_backward(self, secs):
        self.move_a_bit("backward", secs)

    def move_a_bit_turn_left(self, secs):
        self.move_a_bit("turn_left", secs)

    def move_a_bit_turn_right(self, secs):
        self.move_a_bit("turn_right", secs)

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

    def set_room(self, selected_room_id, selected_room_name):

        data = {
            'selected_room_id': selected_room_id,
            'selected_room_name': selected_room_name
        }

        command_path = 'room'
        self.queue_of_command_paths.put((command_path, data))

    def set_door(self, selected_door_id, selected_door_name):

        data = {
            'selected_door_id': selected_door_id,
            'selected_door_name': selected_door_name
        }

        command_path = 'door'
        self.queue_of_command_paths.put((command_path, data))

    def set_room_list(self, room_list):

        data = room_list
        command_path = 'room_list'
        self.queue_of_command_paths.put((command_path, data))

    def set_door_list(self, door_list):

        data = door_list
        command_path = 'door_list'
        self.queue_of_command_paths.put((command_path, data))

    def execute_command_path_get(self, command_path):
        print(f'Command GET: {command_path}')
        response = requests.get(f'http://{self.host}:{self.port}/{command_path}')
        print(f'Response GET: {response.status_code}')
        return response.json()

    def get_room(self):
        return self.execute_command_path_get("room")

    def get_door(self):
        return self.execute_command_path_get("door")

    def get_room_list(self):
        return self.execute_command_path_get("room_list")

    def get_door_list(self):
        return self.execute_command_path_get("door_list")

