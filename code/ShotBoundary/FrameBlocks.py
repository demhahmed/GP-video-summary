import cv2
import numpy as np


def getFrameBlocks(frame, height, width):
    frameBlocks = []
    for r in range(0, height - 32, 32):
        for c in range(0, width - 32, 32):
            window = frame[r:r+32, c:c+32]
            frameBlocks.append(window)
    return frameBlocks
