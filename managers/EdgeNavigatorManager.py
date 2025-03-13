from tools.EdgeDetector import EdgeDetector
from tools.geometry.Line import Line


class EdgeNavigatorManager:

    @staticmethod
    def process_image(image_pil):

        image_width = image_pil.size[0]
        list_lines = EdgeNavigatorManager.get_close_to_horizontal_lines(image_pil)

        set_intersection_x = EdgeNavigatorManager.get_set_intersection_x_of_lines_in_width(list_lines, image_width)
        set_intersection_x.add(0)
        set_intersection_x.add(image_width)
        map_x_min_y = {}

        for intersection_x in set_intersection_x:
            min_y = EdgeNavigatorManager.get_min_value_y(intersection_x, list_lines)
            map_x_min_y[intersection_x] = min_y

        x_with_max_y = EdgeNavigatorManager.get_x_with_max_y(map_x_min_y)
        peronage_max = x_with_max_y / image_width
        print(f"set_intersection_x = {set_intersection_x}")
        print(f"map_x_min_y = {map_x_min_y}")
        print(f"peronage_max = {peronage_max}")

    @staticmethod
    def get_x_with_max_y(map_x_y):

        max_y = float('-inf')
        x_with_max_y = None

        for x, y in map_x_y.items():
            if y > max_y:
                max_y = y
                x_with_max_y = x

        return x_with_max_y

    @staticmethod
    def get_min_value_y(x, list_lines):

        min_y = float('inf')

        for line in list_lines:
            y = line.get_y(x)
            if y < min_y:
                min_y = y

        return min_y

    @staticmethod
    def get_set_intersection_x_of_lines_in_width(list_lines, image_width):

        set_intersection_x = set()

        for line1 in list_lines:
            for line2 in list_lines:
                x, y = line1.intersection(line2)
                if 0 < x < image_width:
                    set_intersection_x.add(x)

        return set_intersection_x

    @staticmethod
    def get_close_to_horizontal_lines(image_pil):

        image_umat = EdgeDetector.image_pil_to_umat(image_pil)
        edges = EdgeDetector.get_horizontal_edges(image_umat, show=True)
        list_lines = []

        image_height = image_pil.size[1]

        for p1i, p2i in edges:
            # Transform from image coordinate system to euclidean coordinate system
            p1 = (p1i[0], image_height - p1i[1])
            p2 = (p2i[0], image_height - p2i[1])

            line = Line(p1, p2)
            list_lines.append(line)

        return list_lines

