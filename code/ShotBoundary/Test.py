import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *

from HistogramCompare import *
from dominantColor import *


frame1 = cv2.imread(
    'frame3795.jpg')
frame2 = cv2.imread(
    'frame3800.jpg')

cv2.imwrite('fram1binary.jpg',getDominantColor(frame1))
cv2.imwrite('fram2binary.jpg',getDominantColor(frame2))

print(HistogramCompare(frame1, frame2))


print((getDominantColorRatio(frame1),getDominantColorRatio(frame2)))
