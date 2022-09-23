import cv2
import time
import os
import HandTrackingModule as htm

wCam,hCam=640,480

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPath='images'
myList=os.listdir(folderPath)
#print(myList)
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime=0
detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]

while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    #print(lmList)
    if len(lmList)!=0:
        fingures = []

        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingures.append(1)
        else:
            fingures.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingures.append(1)
            else:
                fingures.append(0)


        #print(fingures)
        totalFingures=fingures.count(1)
        print(totalFingures)

        h, w, c = overlayList[totalFingures-1].shape
        img[0:h, 0:w] = overlayList[totalFingures-1]

        #cv2.rectangle(img,(20,450),(100,425),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingures),(6,450),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),15)



    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0,2),5)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break