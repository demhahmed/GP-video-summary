import cv2
import numpy as np
from FrameSkipping import FrameCapture
from FrameBlocks import getFrameBlocks
from FrameBlocks import getDominantColorRatio

frame1 = cv2.imread(
    'C:/Users\\medo\\Desktop\\GP REPO\\GP-video-summary\\code\\ShotBoundary\\frame_test\\frame160.jpg')
frame2 = cv2.imread(
    'C:/Users\\medo\\Desktop\\GP REPO\\GP-video-summary\\code\\ShotBoundary\\frame_test\\frame530.jpg')
frame3 = cv2.imread(
    'C:/Users\\medo\\Desktop\\GP REPO\\GP-video-summary\\code\\ShotBoundary\\frame_test\\frame1740.jpg')


print(getDominantColorRatio(frame1))
print(getDominantColorRatio(frame2))
print(getDominantColorRatio(frame3))
