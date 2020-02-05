import cv2
import numpy as np
import FrameSkipping as ExtractFrames
from FrameBlocks import getFrameBlocks
from HistogramCompare import *


path = 'C://Users\medo\Desktop\\test3.mp4'
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
last_frame = -50
print(len(frames))

for i in range(len(frames)-1):
    frame_number = i*step
    frame1 = frames[i]
    frame2 = frames[i+1]

    intersect, corr = HistogramCompare(frame1, frame2)

    if intersect < 4 and corr > 4:
        cuts.append((frame_number, "logo"))
    elif corr < 4 and frame_number - last_frame > cutOffset:
        cuts.append((frame_number, "hard cut"))
        last_frame = frame_number


flag = 0
i = 0
while(i < len(cuts)-1):

    if cuts[i][1] == "logo" and cuts[i+1][1] != "logo" and cuts[i][0] != flag:
        cuts.pop(i)
        i += 1
    if cuts[i][1] == "logo" and cuts[i+1][1] == "logo":
        cuts.pop(i+1)
        flag = cuts[i][0]

    else:
        i += 1

for Item in cuts:
    print(Item, sep='/n')
