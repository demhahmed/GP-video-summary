import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *
from HistogramCompare import *
from DominantColor import *
from Audio import *
from moviepy.editor import VideoFileClip, concatenate
from Utill import *


def cutDetector(frame1, frame2):
    intersect, corr = histogramCompare(frame1, frame2)

    if intersect > 6 and corr > 5:
        return False

    frame_blocks_1 = getFrameBlocks(frame1, frame1.shape[0], frame1.shape[1])
    frame_blocks_2 = getFrameBlocks(frame2, frame1.shape[0], frame1.shape[1])

    if blockChangePercentage(frame_blocks_1, frame_blocks_2) >= 30:
        return True
    return False
