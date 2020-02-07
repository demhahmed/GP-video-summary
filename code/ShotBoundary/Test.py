import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *

from HistogramCompare import *
from dominantColor import *


frame1 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame70.jpg')
frame2 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame75.jpg')


width = 1024
height = 574
intersect, corr = histogramCompare(frame1, frame2)

dominant1 = getDominantColorRatio(frame1)
dominant2 = getDominantColorRatio(frame2)


print(abs(dominant1 - dominant2))
print(intersect, corr)

frame_blocks_1 = getFrameBlocks(frame1, height, width)
frame_blocks_2 = getFrameBlocks(frame2, height, width)

print(blockChangePercentage(frame_blocks_1, frame_blocks_2))
