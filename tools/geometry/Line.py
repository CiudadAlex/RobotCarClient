"""
Line in a 2D plane that responds to the function:
y = mx + b
"""


class Line:

    def __init__(self, p1, p2):

        x1 = p1(0)
        y1 = p1(1)
        x2 = p2(0)
        y2 = p2(1)

        self.m = None
        self.b = None
        self.x_only = None

        if x1 == x2:
            self.x_only = x1
        else:
            self.m = (y1 - y2) / (x1 - x2)
            self.b = y1 - self.m * x1

    def get_y(self, x):
        return self.m * x + self.b

    def get_x(self, y):

        if self.x_only is not None:
            return self.x_only

        return (y - self.b) / self.m

    def intersection(self, line):

        m1 = self.m
        b1 = self.b
        m2 = line.m
        b2 = line.b

        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        return x, y

