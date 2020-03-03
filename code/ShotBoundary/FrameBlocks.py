import cv2
import numpy as np
from HistogramCompare import histogramCompare


def block_Change(frame1, frame2):
    count = 0
    for r in range(0, frame1.shape[0], 150):
        for c in range(0, frame2.shape[1], 150):
            window1 = frame1[r:r+150, c:c+150]
            window2 = frame2[r:r+150, c:c+150]
            intersect, corr = histogramCompare(window1, window2)
            if intersect < 4 and corr < 4:
                count += 1

            elif intersect > 4 and corr < 4:
                count += 0.75

            elif intersect > 4 and corr > 4:
                count += 0.25

            elif intersect < 4 and corr > 4:
                count += 0.1

    return (count/28*100)


'''
def getFrameBlocks(frame, height, width):
    frameBlocks = []
    for r in range(0, height, 150):
        for c in range(0, width, 150):
            window = frame[r:r+150, c:c+150]
            frameBlocks.append(window)
    print(len(frameBlocks))
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
'''
