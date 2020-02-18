import numpy as np
import cv2
import serial

VIDEO_URL = 'http://10.7.7.63:4747/video'
PORT_NO = '/dev/ttyACM0'

ard = serial.Serial(PORT_NO, 9600)
cap = cv2.VideoCapture(VIDEO_URL)

x, y = (640, 480)
l, b = (190, 190)
mid_x, mid_y = (369, 261)

p1 = (int(mid_x - l), int(mid_y - b))
p2 = (int(mid_x + l), int(mid_y + b))

path = []

while True:

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(cv2.blur(gray, (3, 3)), cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30,
                                        minRadius=25, maxRadius=30)

    max_r, max_a, max_b = 0, 999, 999

    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for circle in detected_circles[0, :]:
            a, b, r = circle[0], circle[1], circle[2]
            if p1[0] < a < p2[0] and p1[1] < b < p2[1]:
                if r > max_r:
                    max_r = r
                    max_a = a
                    max_b = b
                cv2.circle(frame, (a, b), r, (0, 255, 0), 2)

    pos = str(max_a) + ':' + str(max_b) + '$'
    ard.write(pos.encode())

    print(f"Center - {(max_a, max_b)}, Radius - {max_r}")
    print("--------------------------------------------")

    # cv2.rectangle(frame, p1, p2, (255, 0, 0), 1)  # plot the plate rectangle
    # cv2.circle(frame, (mid_x, mid_y), 3, (255, 255, 0), 3)  # show center point of the rectangle
    # trace the path
    # if max_r != 0:
    #     path.append((max_a, max_b))
    # if len(path) > 100:
    #     path = []
    # for i in path:
    #     cv2.circle(frame, i, 1, (0, 0, 255), 2)

    # plot a line from the center
    # if max_r != 0:
    #     cv2.line(frame, (max_a, max_b), (mid_x, mid_y), (0, 255, 255), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
