from ultralytics import YOLO
from utils.PropertiesReader import PropertiesReader


class ModelGenerator:

    @staticmethod
    def train_model_rooms(epochs=50):
        properties_reader = PropertiesReader.get_instance()

        train_base_model = "yolov8s"
        model_path = f"./.models/{train_base_model}.pt"
        yaml_path = properties_reader.room_dataset_path + "/data.yaml"

        ModelGenerator.train_new_model(model_path, yaml_path, epochs)

    @staticmethod
    def train_new_model(model_path, yaml_path, epochs):

        # Load a model
        model = YOLO(model_path)

        # Train the model
        return model.train(data=yaml_path, epochs=epochs)

