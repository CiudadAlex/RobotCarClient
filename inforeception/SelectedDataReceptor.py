

class SelectedDataReceptor:

    instance = None

    @staticmethod
    def get_instance():

        if SelectedDataReceptor.instance is None:
            SelectedDataReceptor.instance = SelectedDataReceptor()

        return SelectedDataReceptor.instance

    def __init__(self):
        self.selected_room_id = None
        self.selected_room_name = None

        self.selected_door_id = None
        self.selected_door_name = None

