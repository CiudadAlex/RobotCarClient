from clients.CommandsClient import CommandsClient


class SelectedDataReceptor:

    instance = None

    @staticmethod
    def get_instance():

        if SelectedDataReceptor.instance is None:
            SelectedDataReceptor.instance = SelectedDataReceptor()

        return SelectedDataReceptor.instance

    def __init__(self):
        self.commands_client = CommandsClient.get_instance()

    def set_room(self, selected_room_id, selected_room_name):
        self.commands_client.set_room(selected_room_id, selected_room_name)

    def set_door(self, selected_door_id, selected_door_name):
        self.commands_client.set_door(selected_door_id, selected_door_name)

    def get_room(self):
        return self.commands_client.get_room()

    def get_door(self):
        return self.commands_client.get_door()

