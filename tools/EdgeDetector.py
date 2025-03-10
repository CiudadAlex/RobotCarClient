import cv2 as cv
import numpy as np
import math


class EdgeDetector:

    @staticmethod
    def get_horizontal_edges(image_path, low_threshold=70, high_threshold=120, max_angle_degree=15):
        EdgeDetector.get_edges(image_path, low_threshold, high_threshold, max_angle_degree, True)

    @staticmethod
    def get_vertical_edges(image_path, low_threshold=70, high_threshold=120, max_angle_degree=15):
        EdgeDetector.get_edges(image_path, low_threshold, high_threshold, max_angle_degree, False)

    @staticmethod
    def get_edges(image_path, low_threshold=70, high_threshold=120, max_angle_degree=15, horizontal_or_vertical=True):

        image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

        edges = cv.Canny(image, low_threshold, high_threshold, None, 3)
        hough_lines_p = cv.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)
        list_edges = []

        if hough_lines_p is not None:
            for i in range(0, len(hough_lines_p)):

                l = hough_lines_p[i][0]

                # Here l contains x1,y1,x2,y2  of your line
                point1 = (l[0], l[1])
                point2 = (l[2], l[3])
                angle_degree = EdgeDetector.calculate_angle_degree(point1, point2)

                if -max_angle_degree < angle_degree < max_angle_degree:
                    print("line degree", angle_degree)
                    print(" >> points: ", point1, point2)
                    list_edges.append((point1, point2))
                    cv.line(image, point1, point2, (0, 0, 255), 1, cv.LINE_AA)

        cv.imshow("Source", image)
        return list_edges

    @staticmethod
    def calculate_angle_degree(point1, point2):

        p1 = np.array([point1[0], point1[1]])
        p2 = np.array([point2[0], point2[1]])

        p3 = np.subtract(p2, p1)

        angle_radians = math.atan2(p3[1], p3[0])
        angle_degree = angle_radians * 180 / math.pi
        return angle_degree
