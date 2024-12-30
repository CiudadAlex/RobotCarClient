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

        selected_room_id = SelectedDataReceptor.get_instance().selected_room_id
        selected_room_name = SelectedDataReceptor.get_instance().selected_room_name

        if selected_room_id is None:
            print("No selected ROOM")
            return

        uuid4 = "uuid4"
        image_file_name = f'{selected_room_name}_{uuid4}.png'

        last_image = CarInformationReceptor.get_instance().last_image
        last_image.save(f'{self.images_path}/{image_file_name}.png')

        with open(f'{self.labels_path}/{image_file_name}.txt', 'w') as labels_file:
            labels_file.write(f'{selected_room_id} 0.5 0.5 1 1\n')

    # FIXME finish
