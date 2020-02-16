import cv2

cap = cv2.VideoCapture('http://192.168.43.194:4747/video')
# cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


