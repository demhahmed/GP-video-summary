import cv2
import numpy as np

HUE_LOWER = 0.15
HUE_UPPER = 0.4
INTENSITY_LOWER = 0.2
INTENSITY_UPPER = 0.6
SATURATION_LOWER = 0.1
SATURATION_UPPER = 1


def histogram_intersection(h1, h2):
    sm = 0
    for i in range(13):
        sm += min(h1[i], h2[i])
    return sm


def getFrameBlocks(frame, height, width):
    frameBlocks = []
    for r in range(0, height - 32, 32):
        for c in range(0, width - 32, 32):
            window = frame[r:r+32, c:c+32]
            frameBlocks.append(window)
    return frameBlocks


def getDominantColorRatio(frame):
    # converting the middle pannel into HSI
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

    hue = frame[:, :, 0]/255
    intensity = frame[:, :, 1]/255
    saturation = frame[:, :, 2]/255

    green = (hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (intensity <
                                                                                     INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER)
    frame[(green)] = 255
    frame[~((hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (
        intensity < INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER))] = 0

    frame = cv2.cvtColor(frame, cv2.COLOR_HLS2BGR)   # RGB color to HLS
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # RGB color to gray level

    print(frame.shape)

    percentage = np.sum(frame == 255) / \
        (frame.shape[0]*frame.shape[1])
    # percentage = sum(x.count(255) for x in frame) / \
    # (frame.shape[0]*frame.shape[1])

    return percentage
