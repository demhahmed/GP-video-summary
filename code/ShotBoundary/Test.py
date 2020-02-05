import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *

from HistogramCompare import *
from dominantColor import *


frame1 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame8060.jpg')
frame2 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame8065.jpg')


print(HistogramCompare(frame1, frame2))


print(getDominantColorRatio(frame1))
print(getDominantColorRatio(frame2))
