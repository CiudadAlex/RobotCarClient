from remotecontrolui.RemoteControlUI import RemoteControlUI
from engine.Engine import Engine


online = True


if __name__ == "__main__":
    Engine.start(car_speaks=False,
                 connect_to_video_stream=online,
                 connect_to_audio_stream=online,
                 connect_to_text_stream=online)

    RemoteControlUI.launch()


# FIXME test: generate corpus with val and test images
# FIXME Room recognizer: redo training with higher look

# FIXME Edge recognition to guide.
# FIXME Wall follower

# FIXME ComplexCommandGoToRoom (Door recognition model)


# FIXME revise espeak (makes 360 hang)
'''
import time
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import math

image_path = 'C:/Alex/Dev/data_corpus/VideoCamera/room_dataset_v0/train/images/kitchen_68fb62e4-e427-441a-a814-888d35da6887.png.png'
image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
assert image is not None, "file could not be read, check with os.path.exists()"

before = time.time()
edges = cv.Canny(image, 70, 120, None, 3)
after = time.time()
linesP = cv.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)

if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]

        #here l contains x1,y1,x2,y2  of your line
        #so you can compute the orientation of the line
        p1 = np.array([l[0],l[1]])
        p2 = np.array([l[2],l[3]])

        p0 = np.subtract( p1,p1 ) #not used
        p3 = np.subtract( p2,p1 ) #translate p2 by p1

        angle_radiants = math.atan2(p3[1],p3[0])
        angle_degree = angle_radiants * 180 / math.pi

        print("line degree", angle_degree)

        if 0 < angle_degree < 15 or 0 > angle_degree > -15 :
            print(" >> points: ", l[0], l[1], l[2], l[3])
            cv.line(image,  (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)


cv.imshow("Source", image)

print("Press any key to close")
cv.waitKey(0)
cv.destroyAllWindows()
'''
'''
plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edges, cmap='gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
'''