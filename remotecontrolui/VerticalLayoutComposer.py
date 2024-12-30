
class VerticalLayoutComposer:

    def __init__(self, left_margin, initial_vertical_position, vertical_step, width, height):
        self.left_margin = left_margin
        self.initial_vertical_position = initial_vertical_position
        self.vertical_step = vertical_step

        self.width = width
        self.height = height

        self.index = 0

    def get_next_position(self):

        vertical_position = self.initial_vertical_position + self.vertical_step * self.index

        self.index = self.index + 1

        return self.left_margin, vertical_position

    def get_size(self):
        return self.width, self.height

