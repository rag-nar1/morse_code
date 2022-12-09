import numpy as np
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import matplotlib.pyplot as plt

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
cap = cv2.VideoCapture('/home/ragnar/Desktop/code/sample1.mp4')
detector = FaceMeshDetector(maxFaces=1)
blink=[]
counter=0
lenghtes=[]
plotY = LivePlot(640, 360, [20, 50], invert=True)
while 1 :

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret,frame=cap.read()
    
    frame ,faces=detector.findFaceMesh(frame)
    if faces:
        face=faces[0]
        for id in idList:
            cv2.circle(frame, face[id], 3,(255,0,255), cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtes.append(lenghtVer)
        cv2.line(frame, leftUp, leftDown, (0, 200, 0), 3)

    frame= cv2.resize(frame,(800,600))
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF== ord('z'):
        break

cap.release()
cv2.destroyAllWindows()

mean=sum(lenghtes)/len(lenghtes)
for i in range(len(lenghtes)):
    if lenghtes[i]<mean:
        lenghtes[i]=int(0)
        counter+=1
    elif lenghtes[i]>mean:
        lenghtes[i]=int(2)
        if(counter>11):
            blink.append(3)
        elif(counter>5):
            blink.append(1)
        counter=0
    else :
        lenghtes[i]=int(1)
        counter=0

print(lenghtes)
print(blink)
plt.plot(lenghtes,'o')
plt.show()