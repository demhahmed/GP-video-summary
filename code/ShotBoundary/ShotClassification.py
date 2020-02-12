import numpy as np
import cv2
from dominantColor import getDominantColor
from face import *


def InOut(GrassRatio):
    if GrassRatio < 0.20:
        return 'out'
    else:
        return 'in'


def frameClassification(frame):

    frame = getDominantColor(frame)

    heightRatio = int(frame.shape[0]/11)
    widthRatio = int(frame.shape[1]/11)

    col1 = frame[:, 0:widthRatio*3]
    col2 = frame[:, widthRatio*3:widthRatio*8]
    col3 = frame[:, widthRatio*8:widthRatio*11]

    mid_row = frame[heightRatio*3:heightRatio*11, :]
    last_row = frame[heightRatio*8:heightRatio*11, :]

    GR_1 = np.sum(col1 == 255) / \
        (col1.shape[0]*col1.shape[1])
    GR_2 = np.sum(col2 == 255) / \
        (col2.shape[0]*col2.shape[1])
    GR_3 = np.sum(col3 == 255) / \
        (col3.shape[0]*col3.shape[1])

    GR_mid = np.sum(mid_row == 255) / \
        (mid_row.shape[0]*mid_row.shape[1])

    GR_mid = np.sum(mid_row == 255) / \
        (mid_row.shape[0]*mid_row.shape[1])

    GR_last = np.sum(last_row == 255) / \
        (last_row.shape[0]*last_row.shape[1])

    return GR_1, GR_2, GR_3, GR_mid, GR_last


def shotClassification(frames):
    frame_class = []
    for i, frame in enumerate(frames):
        grassRatio = getDominantColorRatio(frame)
        if grassRatio < 0.2:
            frame_class.append('out')
        else:
            faces, face = faceDetect(frame)
            if grassRatio > 0.7 and faces == 0:
                frame_class.append('long')
            elif grassRatio > 0.4 and faces != 0:
                frame_class.append('close')
    return max(set(frame_class), key=frame_class.count)
