import cv2
import numpy as np
from HistogramCompare import histogramCompare


def getFrameBlocks(frame, height, width):
    frameBlocks = []
    for r in range(0, height, 150):
        for c in range(0, width, 150):
            window = frame[r:r+150, c:c+150]
            frameBlocks.append(window)

    return frameBlocks


def blockChange(block1, block2):
    intersect, corr = histogramCompare(block1, block2)

    if intersect < 4 and corr < 4:
        return True, True
    elif intersect > 4 and corr < 4:
        return (False, True)
    elif intersect > 4 and corr > 4:
        return (True, False)
    else:
        return (False, False)


def blockChangePercentage(frameBlocks1, frameBlocks2):
    count = 0
    for block1, block2 in zip(frameBlocks1, frameBlocks2):
        inter, corr = blockChange(block1, block2)

        if inter and corr:
            count += 1
        elif (corr and not inter):
            count += 0.75
        elif (inter and not corr):
            count += 0.25

    return (count/len(frameBlocks1))*100
