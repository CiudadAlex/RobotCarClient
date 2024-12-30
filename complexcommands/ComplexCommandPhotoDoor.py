from inforeception.SelectedDataReceptor import SelectedDataReceptor
from inforeception.CarInformationReceptor import CarInformationReceptor
import threading


class ComplexCommandPhotoDoor:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandPhotoDoor.instance is None:
            ComplexCommandPhotoDoor.instance = ComplexCommandPhotoDoor()

        return ComplexCommandPhotoDoor.instance

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommandPhotoDoor!!!!!!!")
        self.save_image_in_corpus()

    def save_image_in_corpus(self):

        selected_door_id = SelectedDataReceptor.get_instance().selected_door_id
        selected_door_name = SelectedDataReceptor.get_instance().selected_door_name

        if selected_door_id is None:
            print("No selected DOOR")
            return

        uuid4 = "uuid4"
        image_file_name = f'{selected_door_name}_{uuid4}.png'

        last_image = CarInformationReceptor.get_instance().last_image
        last_image.save(f'{self.images_path}/{image_file_name}.png')

        with open(f'{self.labels_path}/{image_file_name}.txt', 'w') as labels_file:
            labels_file.write(f'{selected_door_id} 0.5 0.5 1 1\n')

    # FIXME finish
