import cv2
import numpy as np



def getDominantColor(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
    ## slice the green
    imask = mask>0
    frame[imask] = 255
    frame[~imask] = 0
    #frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)   # RGB color to HLS
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # RGB color to gray level
    ret, frame = cv2.threshold(frame, 127, 255, 0)
    
    return frame


def getDominantColorRatio(frame):
    frame = getDominantColor(frame)
    percentage = np.sum(frame == 255) / \
        (frame.shape[0]*frame.shape[1])
    return percentage
