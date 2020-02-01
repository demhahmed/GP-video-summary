import cv2
import numpy as np
from FrameSkipping import FrameCapture
from FrameBlocks import getFrameBlocks

frame1 = cv2.imread(
    'C:/Users\\medo\\Desktop\\GP REPO\\GP-video-summary\\code\\ShotBoundary\\frame_test\\frame810.jpg')
frame2 = cv2.imread(
    'C:/Users\\medo\\Desktop\\GP REPO\\GP-video-summary\\code\\ShotBoundary\\frame_test\\frame820.jpg')


frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HLS)
frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HLS)
frame1_blocks = getFrameBlocks(frame1, frame1.shape[0], frame1.shape[1])
frame2_blocks = getFrameBlocks(frame2, frame1.shape[0], frame1.shape[1])

block_change = [cv2.absdiff(x, y)
                for x, y in zip(frame1_blocks, frame2_blocks)]
block_change_average = [np.mean(x) for x in block_change]
print(np.mean(block_change_average))
