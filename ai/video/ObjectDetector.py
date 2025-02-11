from ultralytics import YOLO
import math
import os


class ObjectDetector:

    def __init__(self, model_path):
        os.environ['YOLO_VERBOSE'] = 'False'
        self.model = YOLO(model_path, verbose=False)

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

                class_id = int(box.cls[0])
                class_name_box = r.names[class_id]

                if class_name_box == class_name:
                    return True

        return False

    @staticmethod
    def count_number_object_class(results, class_name):

        count = 0

        for r in results:
            boxes = r.boxes

            for box in boxes:

                class_id = int(box.cls[0])
                class_name_box = r.names[class_id]

                if class_name_box == class_name:
                    count = count + 1

        return count

    @staticmethod
    def get_list_class_and_confidence(results):

        list_class_and_confidence = []

        for r in results:
            boxes = r.boxes

            for box in boxes:

                confidence = math.ceil((box.conf[0] * 100)) / 100
                class_id = int(box.cls[0])
                class_name_box = r.names[class_id]

                list_class_and_confidence.append((class_name_box, confidence))

        list_class_and_confidence_ordered = sorted(list_class_and_confidence, key=lambda x: x[1], reverse=True)

        return list_class_and_confidence_ordered

    @staticmethod
    def get_most_confident_class(results):

        most_confident_class_name = None
        max_confidence = -1

        for r in results:
            boxes = r.boxes

            for box in boxes:
                confidence = math.ceil((box.conf[0] * 100)) / 100
                class_id = int(box.cls[0])
                class_name_box = r.names[class_id]

                if confidence > max_confidence:
                    max_confidence = confidence
                    most_confident_class_name = class_name_box

        return most_confident_class_name

    @staticmethod
    def print_results(results):

        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                confidence = math.ceil((box.conf[0] * 100)) / 100

                class_id = int(box.cls[0])
                class_name_box = r.names[class_id]

                print(f"Class name: {class_name_box}. Confidence: {confidence}"
                      f". Window ---> (x1, y1) = ({x1}, {y1}), (x2, y2) = ({x2}, {y2})")

    @staticmethod
    def get_bounding_box_vertices_of_single_object_of_class(results, class_name):

        if ObjectDetector.count_number_object_class(results, class_name) != 1:
            return None

        for r in results:
            boxes = r.boxes

            for box in boxes:

                class_id = int(box.cls[0])
                class_name_box = r.names[class_id]

                if class_name_box == class_name:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                    return (x1, y1), (x2, y2)

    @staticmethod
    def show_results(results):
        for r in results:
            r.show()  # Display the image with predictions
