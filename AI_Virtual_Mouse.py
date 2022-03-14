import cv2
import numpy as np
import Hand_Tracking_Module as htm
import time
import autopy
# import mediapipe as mp
################################
wCam, hCam = 640, 480
frameR = 100 #Frame Reduction
smoothening = 7

######################################

pTime = 0
plocX,plocY = 0,0
clocX, cloxY = 0, 0



cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)


detector = htm.handDetector(maxHands = 1)
wScr, hScr = autopy.screen.size()
print(wScr,hScr)
while True:
    # Find the Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)
    # Get the tip of the middle & index fingers

    if len(lmlist) != 0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        # print(x1,y1,x2,y2)
    # Which fingers are Up.
        fingers = detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR), (wCam-frameR, hCam - frameR), (255,0,255), 2)
        # print(fingers)
    # Only Index Finger (in moving mode)
        if fingers[1] == 1 and fingers[2] == 0:
        #Convert Coordinates
            
            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR),(0,hScr))

        #Smoothen the values (prevent flickering)
            clocX = plocX + (x3 - plocX)/smoothening
            clocY = plocY + (y3 - plocY)/smoothening

        #Move mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img,(x1,y1),15,(0,255,0), cv2.FILLED)
            plocX, plocY = clocX, clocY
    #Both index and middle fingers are up: Clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            #find the distance between fingers
            length, img, lineInfo = detector.findDistance(8,12,img)
            print(length)
            # distance is short then click mouse
            if length< 30:
                cv2.circle(img, (lineInfo[4],lineInfo[5]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.click()
        

    # Frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    #Display the video feed
    cv2.imshow("Image",img)
    cv2.waitKey(1)
