import os
import uuid


class YoloDatasetBuilder:

    def __init__(self, dataset_path, list_classes):
        self.dataset_path = dataset_path
        self.list_classes = list_classes

        train_path = f'{self.dataset_path}/train'
        self.images_path = f'{train_path}/images'
        self.labels_path = f'{train_path}/labels'

        self.data_yaml_path = f'{self.dataset_path}/data.yaml'

    def build_structure(self):

        os.makedirs(self.images_path, exist_ok=True)
        os.makedirs(self.labels_path, exist_ok=True)

        if not os.path.exists(self.data_yaml_path):
            with open(self.data_yaml_path, 'w') as data_yaml_file:
                data_yaml_file.write(f'train: ../train/images\n\nnc: {len(self.list_classes)}\nnames: {self.list_classes}')

    def save_image_in_corpus(self, image, class_id, class_name):

        uuid4 = uuid.uuid4()
        image_file_name = f'{class_name}_{uuid4}.png'

        image.save(f'{self.images_path}/{image_file_name}.png')

        with open(f'{self.labels_path}/{image_file_name}.txt', 'w') as labels_file:
            labels_file.write(f'{class_id} 0.5 0.5 1 1\n')

