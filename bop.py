import numpy as np
import cv2

cap = cv2.VideoCapture('http://10.7.7.63:4747/video')

x = 640
y = 480

l, b = 190, 190
# b = 200

p1 = (int(x / 2 - l), int(y / 2 - b))
p2 = (int(x / 2 + l), int(y / 2 + b))
path = []

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(cv2.blur(gray, (3, 3)), cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30,
                                        minRadius=25, maxRadius=30)

    max_r, max_a, max_b = 0, 320, 240

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
    path.append((max_a, max_b))
    print("Circle: radius - ", max_r, "Center - ", (max_a, max_b))
    print("--------------------------------------------")

    # Display the resulting frame
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 1)
    if len(path) > 80:
        path = []
    for i in path:
        cv2.circle(frame, i, 1, (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#
# color = np.uint8([[[0, 255, 0]]])
# hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
# lower_col = np.array([hsv_color[0][0][0] - 10, 10, 10])
# upper_col = np.array([hsv_color[0][0][0] + 10, 255, 255])
#
# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     # Our operations on the frame come here
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     # mask = cv2.inRange(hsv, lower_col, upper_col)
#     mask = cv2.inRange(hsv, np.array([0, 0, 212]), np.array([131, 255, 255]))
#
#     # Display the resulting frame
#     cv2.rectangle(frame, p1, p2, (255, 0, 0), 1)
#     center_y, center_x = np.nonzero(mask)
#     if len(center_x) < 200:
#         center = (320, 640)
#     else:
#         center = int(np.mean(center_x)), int(np.mean(center_y))
#     print(center)
#     path.append(center)
#     cv2.circle(frame, center, 5, (0, 0, 0), 5)
#     cv2.circle(mask, center, 5, (0, 0, 0), 5)
#
#     for p in path:
#         cv2.circle(frame, p, 1, (0, 0, 255), 2)
#
#     cv2.imshow('frame', frame)
#     cv2.imshow('mask', cv2.blur(mask, (5, 5)))
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
