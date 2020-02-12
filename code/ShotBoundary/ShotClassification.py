import numpy as np
import cv2

from dominantColor import getDominantColor
def InOut(GrassRatio):
    if GrassRatio < 0.20:
        return 'out'
    else:
        return 'in'

def frameClassification(frame):
    frame = getDominantColor(frame)

    heightRatio = int(frame.shape[0]/10)
    widthRatio = int(frame.shape[1]/10)

    img1 = frame[heightRatio*2:heightRatio*8,0:widthRatio*2]
    img2 = frame[heightRatio*2:heightRatio*8,widthRatio*2:widthRatio*8]
    img3 = frame[heightRatio*2:heightRatio*8,widthRatio*8:widthRatio*10]

    GR_1 = np.sum(img1 == 255) / \
    (img1.shape[0]*img1.shape[1])
    GR_2 = np.sum(img2 == 255) / \
    (img2.shape[0]*img2.shape[1])
    GR_3 = np.sum(img3 == 255) / \
    (img3.shape[0]*img3.shape[1])

    Rdiff = 0.5 * (abs(GR_1-GR_2)+abs(GR_2-GR_3))

    return GR_1 , GR_2, GR_3 ,Rdiff


