

class Aggregator:

    def __init__(self):
        self.map = {}

    def add(self, key, value_to_add):

        if key not in self.map:
            self.map[key] = 0

        self.map[key] = self.map[key] + value_to_add

    def get_key_of_max_value(self):

        max_count = -1
        key_max_value = None

        for key, count in self.map.items():
            if count > max_count:
                max_count = count
                key_max_value = key

        return key_max_value

