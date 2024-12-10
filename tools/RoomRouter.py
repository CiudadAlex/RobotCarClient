from utils.PropertiesReader import PropertiesReader


class RoomRouter:

    def __init__(self):
        self.map_routes = self.build_map_routes()

    def build_map_routes(self):

        properties_reader = PropertiesReader.get_instance()
        list_room = properties_reader.room_list.split(",")
        list_adjacency = properties_reader.room_adjacency.split(",")

        map_routes = {}

        for adjacency in list_adjacency:

            list_adjacency_items = adjacency.split(":")
            room1 = list_adjacency_items[0]
            room2 = list_adjacency_items[1]

            if room1 not in list_room or room2 not in list_room:
                raise Exception(f"Either '{room1}' or '{room2}' are not in the list {list_room}")

            self.add_adjacency_to_map_routes(map_routes, room1, room2)
            self.add_adjacency_to_map_routes(map_routes, room2, room1)

        return map_routes

    @staticmethod
    def add_adjacency_to_map_routes(map_routes, room1, room2):

        if room1 not in map_routes:
            map_routes[room1] = []

        map_routes[room1].append(room2)
