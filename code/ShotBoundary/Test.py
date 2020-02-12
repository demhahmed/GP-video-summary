import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *

from HistogramCompare import *
from dominantColor import *


frame1 = cv2.imread(
    'frame250.jpg')
'''
frame2 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame10890.jpg')

cv2.imwrite('fram1binary.jpg', getDominantColor(frame1))
cv2.imwrite('fram2binary.jpg', getDominantColor(frame2))

width = 1024
height = 574
intersect, corr = histogramCompare(frame1, frame2)
'''
dominant1 = getDominantColorRatio(frame1)
#dominant2 = getDominantColorRatio(frame2)


print(dominant1)
#print(intersect, corr)

#frame_blocks_1 = getFrameBlocks(frame1, height, width)
#frame_blocks_2 = getFrameBlocks(frame2, height, width)

