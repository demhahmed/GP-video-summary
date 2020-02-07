import cv2
import numpy as np
from HistogramCompare import histogramCompare


def getFrameBlocks(frame, height, width):
    frameBlocks = []
    for r in range(0, height - 32, 32):
        for c in range(0, width - 32, 32):
            window = frame[r:r+32, c:c+32]
            frameBlocks.append(window)
    return frameBlocks


def blockChange(block1, block2):
    intersect, corr = histogramCompare(block1, block2)
    if corr < 5:
        return True


def blockChangePercentage(frameBlocks1, frameBlocks2):
    count = 0
    for block1, block2 in zip(frameBlocks1, frameBlocks2):
        if blockChange(block1, block2):
            count += 1
    return (count/len(frameBlocks1))*100
