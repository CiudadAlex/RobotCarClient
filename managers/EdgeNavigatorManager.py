from tools.EdgeDetector import EdgeDetector
from tools.geometry.Line import Line


class EdgeNavigatorManager:

    def process_image(self, pil_image):

        image_umat = EdgeDetector.image_pil_to_umat(pil_image)
        edges = EdgeDetector.get_horizontal_edges(image_umat, show=True)
        list_lines = []
        image_height = pil_image.size[1]

        for p1i, p2i in edges:

            # Transform from image coordinate system to euclidean coordinate system
            p1 = (p1i[0], image_height - p1i[1])
            p2 = (p2i[0], image_height - p2i[1])

            line = Line(p1, p2)
            list_lines.append(line)


