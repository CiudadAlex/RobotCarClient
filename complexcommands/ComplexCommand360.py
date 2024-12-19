from clients.CommandsClient import CommandsClient
from utils.PropertiesReader import PropertiesReader
import time
import os
import uuid


class ComplexCommand360:

    number_of_steps = 20

    time_sleep_move = 0.3
    time_sleep_adjust_image = 1.5

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommand360.instance is None:
            ComplexCommand360.instance = ComplexCommand360()

        return ComplexCommand360.instance

    def __init__(self):
        self.running = False
        self.last_image = None
        self.id_selected_room = None
        self.selected_room = None
        self.commands_client = CommandsClient.get_instance()

        properties_reader = PropertiesReader.get_instance()
        train_path = f'{properties_reader.room_dataset_path}/train'
        self.images_path = f'{train_path}/images'
        self.labels_path = f'{train_path}/labels'
        os.makedirs(self.images_path, exist_ok=True)
        os.makedirs(self.labels_path, exist_ok=True)

    def execute(self):

        self.running = True

        for step in range(ComplexCommand360.number_of_steps):

            if not self.running:
                return

            self.move_step()
            self.save_image_in_corpus()

    def save_image_in_corpus(self):

        if self.id_selected_room is None:
            print("No selected ROOM")
            return

        uuid4 = uuid.uuid4()
        image_file_name = f'{self.selected_room}_{uuid4}.png'

        self.last_image.save(f'{self.images_path}/{image_file_name}.png')

        with open(f'{self.labels_path}/{image_file_name}.txt', 'w') as labels_file:
            labels_file.write(f'{self.id_selected_room} 0.5 0.5 1 1\n')

    def move_step(self):

        self.commands_client.move_turn_left()
        time.sleep(ComplexCommand360.time_sleep_move)
        self.commands_client.move_stop()
        time.sleep(ComplexCommand360.time_sleep_adjust_image)

