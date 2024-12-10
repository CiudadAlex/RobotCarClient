from utils.PropertiesReader import PropertiesReader


class RoomRouter:

    def __init__(self):
        self.map_routes = self.build_map_routes()
        print(f"map_routes = {self.map_routes}")

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

    def create_route(self, room_start, room_end):

        if room_start == room_end:
            return []

        set_visited_rooms = {room_start}
        list_next_rooms = self.map_routes[room_start]
        routes = [list_next_rooms]

        while True:

            routes_next_generation = []

            for route in routes:

                list_expanded_routes = self.get_expanded_routes(route, set_visited_rooms)

                for expanded_route in list_expanded_routes:
                    if self.is_route_finished(expanded_route, room_end):
                        return expanded_route

                routes_next_generation.extend(list_expanded_routes)

            routes = routes_next_generation

    @staticmethod
    def is_route_finished(route, room_end):
        return route[-1] == room_end

    def get_expanded_routes(self, route_unfinished, set_visited_rooms):

        last_room = route_unfinished[-1]
        list_next_rooms = self.map_routes[last_room]
        list_expanded_routes = []

        for next_room in list_next_rooms:

            if next_room not in set_visited_rooms:
                expanded_route = []
                expanded_route.extend(route_unfinished)
                expanded_route.append(next_room)
                set_visited_rooms.add(next_room)
                list_expanded_routes.append(expanded_route)

        return list_expanded_routes

