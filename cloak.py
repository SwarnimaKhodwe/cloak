import cv2
import numpy as np
import time

vid_1 = cv2.VideoCapture(0)

time.sleep(2)  # 2 sec to set the camera according to environment

bg = 0

for i in range(20):  # 20 iterations to capture the background
    ret, bg0 = vid_1.read() #returns the image and true value (capture the background)
    bg = cv2.flip(bg0,+1)

while(vid_1.isOpened()):  # capture the video only when window is open
    ret, img0 = vid_1.read() #cature the image to perform opetatios on it
    img = cv2.flip(img0,+1)

    if not ret:  # if the ret is not returning true
        break  

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #convert the img from BGR to HSV(Hue Saturation Value)

    low_red = np.array([0,120,70])
    upp_red = np.array([10,225,225])
    sep_1 = cv2.inRange(hsv, low_red, upp_red)  #seperating the cloak part from low_red to upp_red

    low_red = np.array([160,120,70])
    upp_red = np.array([180,255,255])
    sep_2 = cv2.inRange(hsv, low_red, upp_red)  #seperating the cloak part from low_red to upp_red

    sep_1 = sep_1 + sep_2  # OR condition is used

    sep_1 = cv2.morphologyEx(sep_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)  # due to MORPH_OPEN noise gets removed from the img

    sep_1 = cv2.morphologyEx(sep_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8),iterations=1)  #due to MORPH_DILATE images gets smoothen

    sep_2 = cv2.bitwise_not(sep_1)  #except cloak part everything gets included

    res1 = cv2.bitwise_and(bg, bg, mask=sep_1 )
    res2 = cv2.bitwise_and(img, img, mask=sep_2)
    op = cv2.addWeighted(res1, 1, res2, 1, 0)
    
    cv2.imshow('OUTPUT',op)
    if cv2.waitKey(1) & 0xFF== ord('z'):
        break

vid_1.release()
cv2.destroyAllWindows()
