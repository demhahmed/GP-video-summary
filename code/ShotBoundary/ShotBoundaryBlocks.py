import cv2
import numpy as np
import FrameSkipping as *
from FrameBlocks import *


path = 'C://Users\medo\Desktop\\test.mp4'
cap = cv2.VideoCapture(path)

if cap.isOpened() == False:
    print('err reading video')

# getting video width, height and FPS
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))

frames = ExtractFrames(path, step=5)
step = 5
cuts = []
cutOffset = 50
last_frame = (-50, "")
print(len(frames))

for i in range(len(frames)-1):
    frame_number = i*step
    frame1 = frames[i]
    frame2 = frames[i+1]

    frame_blocks_1 = getFrameBlocks(frame1, height, width)
    frame_blocks_2 = getFrameBlocks(frame2, height, width)

    if blockChangePercentage(frame_blocks_1, frame_blocks_2) > 75:
        cuts.append(i*step, "hard cut")


for Item in cuts:
    print(Item, sep='/n')
