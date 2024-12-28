

class Counter:

    def __init__(self):
        self.map = {}

    def add(self, key):

        if key not in self.map:
            self.map[key] = 0

        self.map[key] = self.map[key] + 1

    def get_max_count(self):

        max_count = -1
        key_max_count = None

        for key, count in self.map.items():
            if count > max_count:
                max_count = count
                key_max_count = key

        return key_max_count

