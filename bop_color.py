import numpy as np
import cv2
import serial

ard = serial.Serial('/dev/ttyACM0', 9600)

cap = cv2.VideoCapture('http://10.7.7.63:4747/video')
x, y = (640, 480)
l, b = (190, 190)

mid_x, mid_y = (369, 261)

p1 = (int(mid_x - l), int(mid_y - b))
p2 = (int(mid_x + l), int(mid_y + b))

path = []

color = np.uint8([[[0, 255, 0]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
lower_col = np.array([hsv_color[0][0][0] - 10, 10, 10])
upper_col = np.array([hsv_color[0][0][0] + 10, 255, 255])

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # mask = cv2.inRange(hsv, lower_col, upper_col)   # for showing colors other than white
    mask = cv2.inRange(hsv, np.array([0, 0, 212]), np.array([131, 255, 255]))

    # Display the resulting frame
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 1)
    center_y, center_x = np.nonzero(mask)

    if len(center_x) < 200:
        center = (mid_y, mid_y)
    else:
        center = int(np.mean(center_x)), int(np.mean(center_y))

    pos = str(center[0]) + ':' + str(center[1]) + '$'
    ard.write(pos.encode())
    print(f"Center - {(max_a, max_b)}, Radius - {max_r}")
    print("--------------------------------------------")

    cv2.circle(frame, center, 3, (0, 0, 0), 3)
    cv2.circle(mask, center, 3, (0, 0, 0), 3)

    path.append(center)
    for p in path:
        cv2.circle(frame, p, 1, (0, 0, 255), 2)
    if len(path) > 100:
        path = []

    cv2.imshow('frame', frame)
    cv2.imshow('mask', cv2.blur(mask, (5, 5)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
