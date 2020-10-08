import cv2 as cv
import math

cap = cv.VideoCapture(0)

def nothing(x):
    pass

cv.namedWindow("Trackbars")
cv.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
cv.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
cv.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv.createTrackbar("U-V", "Trackbars", 243, 255, nothing)

while True:
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    l_h = cv.getTrackbarPos("L-H", "Trackbars")
    l_s = cv.getTrackbarPos("L-S", "Trackbars")
    l_v = cv.getTrackbarPos("L-V", "Trackbars")
    u_h = cv.getTrackbarPos("U-H", "Trackbars")
    u_s = cv.getTrackbarPos("U-S", "Trackbars")
    u_v = cv.getTrackbarPos("U-V", "Trackbars")

    # lower = (0, 169, 141)
    # upper = (180, 255, 255)
    lower = (l_h, l_s, l_v)
    upper = (u_h, u_s, u_v)

    mask = cv.inRange(hsv, lower, upper)

    cv.imshow("Mask", mask)
    cv.imshow("Frame", frame)

    key = cv.waitKey(1)
    if key == 27:
        break