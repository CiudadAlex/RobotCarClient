import cv2 as cv
import numpy as np
import math


class EdgeDetector:

    @staticmethod
    def get_horizontal_edges(image_umat, low_threshold=70, high_threshold=120, max_angle_degree=15, show=False):
        return EdgeDetector.get_edges(image_umat, low_threshold, high_threshold, max_angle_degree, True, show)

    @staticmethod
    def get_vertical_edges(image_umat, low_threshold=70, high_threshold=120, max_angle_degree=15, show=False):
        return EdgeDetector.get_edges(image_umat, low_threshold, high_threshold, max_angle_degree, False, show)

    @staticmethod
    def image_pil_to_umat(image_pil):
        img_rgb = np.array(image_pil)
        return cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)

    @staticmethod
    def image_path_to_umat(image_path):
        return cv.imread(image_path, cv.IMREAD_GRAYSCALE)

    @staticmethod
    def get_edges(image_umat, low_threshold=70, high_threshold=120, max_angle_degree=15, horizontal_or_vertical=True, show=False):

        edges = cv.Canny(image_umat, low_threshold, high_threshold, None, 3)
        hough_lines_p = cv.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)
        list_edges = []

        if hough_lines_p is not None:
            for i in range(0, len(hough_lines_p)):

                l = hough_lines_p[i][0]

                # Here l contains x1,y1,x2,y2  of your line
                point1 = (l[0], l[1])
                point2 = (l[2], l[3])
                angle_degree = EdgeDetector.calculate_angle_degree(point1, point2)

                if horizontal_or_vertical:
                    central_angle_degree = 0
                else:
                    central_angle_degree = 90

                bottom_angle_degree = central_angle_degree - max_angle_degree
                top_angle_degree = central_angle_degree + max_angle_degree

                if bottom_angle_degree < angle_degree < top_angle_degree:
                    print("line degree", angle_degree)
                    print(" >> points: ", point1, point2)
                    list_edges.append((point1, point2))
                    cv.line(image_umat, point1, point2, (0, 0, 255), 1, cv.LINE_AA)

        if show:
            cv.imshow("Source", image_umat)
            print("Press any key to close")
            cv.waitKey(0)
            cv.destroyAllWindows()

        return list_edges

    @staticmethod
    def calculate_angle_degree(point1, point2):

        p1 = np.array([point1[0], point1[1]])
        p2 = np.array([point2[0], point2[1]])

        p3 = np.subtract(p2, p1)

        angle_radians = math.atan2(p3[1], p3[0])
        angle_degree = angle_radians * 180 / math.pi
        return angle_degree
