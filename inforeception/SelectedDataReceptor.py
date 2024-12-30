

class SelectedDataReceptor:

    instance = None

    @staticmethod
    def get_instance():

        if SelectedDataReceptor.instance is None:
            SelectedDataReceptor.instance = SelectedDataReceptor()

        return SelectedDataReceptor.instance

    def __init__(self):
        self.id_selected_room = None
        self.selected_room = None

        self.selected_door_id = None
        self.selected_door_name = None

