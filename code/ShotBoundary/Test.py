import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *

from HistogramCompare import *

'''
frame1 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame10165.jpg')
frame2 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame10170.jpg')
'''


ExtractFramesToDisk('C:/Users\\medo\\Desktop\\test3.mp4', 5)
