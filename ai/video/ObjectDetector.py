from ultralytics import YOLO
import math


class ObjectDetector:

    def __init__(self, model_path):
        self.model = YOLO(model_path)

    @classmethod
    def load_custom_model(cls, model_name):
        return cls(".models/" + model_name + ".pt")

    @classmethod
    def load_standard_model(cls, size="x"):

        available_sizes = ["n", "s", "m", "l", "x"]

        if size not in available_sizes:
            raise Exception(f"Unrecognized model size: {size}. Available sizes: {available_sizes}")

        return cls(".models/yolov8" + size + ".pt")

    def predict(self, image_path_or_pil_image):
        results = self.model.predict(source=image_path_or_pil_image, conf=0.7)
        return results

    @staticmethod
    def is_there_object_class(results, class_name):

        for r in results:
            boxes = r.boxes

            for box in boxes:

                # class name
                cls = int(box.cls[0])
                class_name_box = r.names[cls]

                if class_name_box == class_name:
                    return True

        return False

    @staticmethod
    def count_number_object_class(results, class_name):

        count = 0

        for r in results:
            boxes = r.boxes

            for box in boxes:

                # class name
                cls = int(box.cls[0])
                class_name_box = r.names[cls]

                if class_name_box == class_name:
                    count = count + 1

        return count

    @staticmethod
    def print_results(results):

        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                confidence = math.ceil((box.conf[0] * 100)) / 100

                # class name
                cls = int(box.cls[0])

                print(f"Class name: {r.names[cls]}. Confidence: {confidence}"
                      f". Window ---> (x1, y1) = ({x1}, {y1}), (x2, y2) = ({x2}, {y2})")

    @staticmethod
    def get_bounding_box_vertices_of_single_object_of_class(results, class_name):

        if ObjectDetector.count_number_object_class(results, class_name) != 1:
            return None

        for r in results:
            boxes = r.boxes

            for box in boxes:

                # class name
                cls = int(box.cls[0])
                class_name_box = r.names[cls]

                if class_name_box == class_name:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                    return (x1, y1), (x2, y2)

    @staticmethod
    def show_results(results):
        for r in results:
            r.show()  # Display the image with predictions
