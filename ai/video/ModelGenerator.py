from ultralytics import YOLO
from utils.PropertiesReader import PropertiesReader


class ModelGenerator:

    @staticmethod
    def train_model_rooms(epochs=50):
        properties_reader = PropertiesReader.get_instance()

        train_base_model_name = "yolov8s"
        dataset_path = properties_reader.room_dataset_path
        ModelGenerator.train_new_model(train_base_model_name, dataset_path, epochs)

    @staticmethod
    def train_model_doors(epochs=50):
        properties_reader = PropertiesReader.get_instance()

        train_base_model_name = "yolov8s"
        dataset_path = properties_reader.door_dataset_path
        ModelGenerator.train_new_model(train_base_model_name, dataset_path, epochs)

    @staticmethod
    def train_new_model(train_base_model_name, dataset_path, epochs):

        model_path = f"./.models/{train_base_model_name}.pt"
        yaml_path = dataset_path + "/data.yaml"

        # Load a model
        model = YOLO(model_path)

        # Train the model
        return model.train(data=yaml_path, epochs=epochs)

