import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#################################
wCam,hCam=640,480
################################

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ptime=0
detector=htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
#print(volRange)
volume.SetMasterVolumeLevel(0, None)
minVol=volRange[0]
maxVol=volRange[1]

minVol=volRange[0]
maxVol=volRange[1]
volBar=400

while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        lenght=math.hypot(x2-x1,y2-y1)
        #print(lenght)


        #hand range was fom 50 to 300
        #15 to 230
        #volume range is from -63 to 0

        vol=np.interp(lenght,[10,230],[minVol,maxVol])
        #print(int(lenght),vol)
        volBar = np.interp(lenght, [10, 230], [400, 150])
        #print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if lenght<15:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)



    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)


    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break