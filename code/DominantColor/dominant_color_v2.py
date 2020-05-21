import cv2
import numpy as np
# defining channels boundries
HUE_LOWER = 0.15
HUE_UPPER = 0.4
INTENSITY_LOWER = 0.2
INTENSITY_UPPER = 0.6
SATURATION_LOWER = 0.1
SATURATION_UPPER = 1


def getDominantColor(frame):
    # converting the middle pannel into HSI
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

    hue = frame[:, :, 0]/255
    intensity = frame[:, :, 1]/255
    saturation = frame[:, :, 2]/255

    frame[(hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (intensity <
                                                                                   INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER)] = 255
    frame[~((hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (
        intensity < INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER))] = 0



def getDominantColorRatio(frame):
    # converting the middle pannel into HSI
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

    hue = frame[:, :, 0]/255
    intensity = frame[:, :, 1]/255
    saturation = frame[:, :, 2]/255

    green = (hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (intensity <
                                                                                     INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER)
    frame[(green)] = 255
    frame[~(green)] = 0

    frame = cv2.cvtColor(frame, cv2.COLOR_HLS2BGR)   # RGB color to HLS
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # RGB color to gray level

    frame = getDominantColor(frame)
    percentage = np.sum(frame == 255) / \
        (frame.shape[0]*frame.shape[1])

    return percentage