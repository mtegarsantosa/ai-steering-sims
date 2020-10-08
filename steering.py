import cv2 as cv
import math
import socketio

cap = cv.VideoCapture(0)
pointsList = [0, 0]

sio = socketio.Client()

@sio.on('connect')
def connect():
   print("connect")

sio.connect('http://localhost:4567')

def getAngle(pointsList):
    pt1, pt2 = pointsList
    angR = math.atan2(-(pt1[0] - pt2[0]), (pt1[1] - pt2[1]))
    angD = round(math.degrees(angR))
    return angD

def centroid(contour, mask):
    for c in contour:
        area = cv.contourArea(c)
        if area > 200:
            M = cv.moments(mask)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return [cX, cY]

def trainingColor(hsv, low, upp, pt):
    mask = cv.inRange(hsv, low, upp)
    contour, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    center = centroid(contour, mask)
    if center != None: pointsList[pt] = center
    # else: pointsList[pt] = [0, 0]

def drawFrame(frame):
    cv.circle(frame, tuple(pointsList[0]), 5, (255, 0, 0), -1)
    cv.circle(frame, tuple(pointsList[1]), 5, (0, 255, 0), -1)
    cv.line(frame, tuple(pointsList[0]), (pointsList[0][0], pointsList[0][1]-100), (0,0,255), 2)
    cv.line(frame, tuple(pointsList[1]), tuple(pointsList[0]), (0,0,255), 2)
    cv.putText(frame, str(pointsList[0]), (pointsList[0][0]-100, pointsList[0][1]), cv.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0),2)
    cv.putText(frame, str(pointsList[1]), (pointsList[1][0]+50, pointsList[1][1]), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0),2)

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Origin Color
    trainingColor(hsv, (0, 98, 171), (73, 255, 255), 0)
    
    # Point Color
    trainingColor(hsv, (21, 77, 81), (81, 255, 255), 1)

    if pointsList[0] != 0 and pointsList[1] != 0:
        drawFrame(frame)
        angle = getAngle(pointsList)
        sio.emit('steering', angle/180/0.5)
        
    cv.imshow("frame", frame)

    key = cv.waitKey(1)
    if key == 27: # ESC BUTTON
        break

sio.wait()