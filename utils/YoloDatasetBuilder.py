import os
import uuid
import random


class YoloDatasetBuilder:

    def __init__(self, dataset_path, list_classes):
        self.dataset_path = dataset_path
        self.list_classes = list_classes

        self.train_path = f'{self.dataset_path}/train'
        self.test_path = f'{self.dataset_path}/test'
        self.valid_path = f'{self.dataset_path}/valid'

        self.data_yaml_path = f'{self.dataset_path}/data.yaml'

    def build_structure(self):

        self.build_sub_structure(self.train_path)
        self.build_sub_structure(self.test_path)
        self.build_sub_structure(self.valid_path)

        if not os.path.exists(self.data_yaml_path):
            with open(self.data_yaml_path, 'w') as data_yaml_file:
                data_yaml_file.write(f'train: ../train/images\n\nnc: {len(self.list_classes)}\nnames: {self.list_classes}')

    def build_sub_structure(self, path):
        os.makedirs(self.get_images_path(path), exist_ok=True)
        os.makedirs(self.get_labels_path(path), exist_ok=True)

    @staticmethod
    def get_images_path(path):
        return f'{path}/images'

    @staticmethod
    def get_labels_path(path):
        return f'{path}/labels'

    def save_image_in_corpus(self, image, class_id, class_name):

        random_1_to_10 = random.randint(1, 10)

        if random_1_to_10 == 1:
            path = self.test_path
        elif random_1_to_10 == 2:
            path = self.valid_path
        else:
            path = self.train_path

        images_path = self.get_images_path(path)
        labels_path = self.get_labels_path(path)

        uuid4 = uuid.uuid4()
        image_file_name = f'{class_name}_{uuid4}.png'

        image.save(f'{images_path}/{image_file_name}.png')

        with open(f'{labels_path}/{image_file_name}.txt', 'w') as labels_file:
            labels_file.write(f'{class_id} 0.5 0.5 1 1\n')

