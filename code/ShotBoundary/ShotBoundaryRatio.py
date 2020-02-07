import cv2
import numpy as np
import FrameSkipping as ExtractFrames
from HistogramCompare import *
from dominantColor import *

path = "C:/Users\\salama\\Desktop\\test.mp4"
cap = cv2.VideoCapture(path)

if cap.isOpened() == False:
    print('err reading video')

# getting video width, height and FPS
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))

frames = ExtractFrames(path, step=6)
step = 6
cuts = []
print(len(frames))

for i in range(len(frames)-1):
    frame_number = i*step
    frame1 = frames[i]
    frame2 = frames[i+1]

    intersect, corr = HistogramCompare(frame1, frame2)

    # getting frame grass ratio
    frame1_GR = getDominantColorRatio(frame1)
    frame2_GR = getDominantColorRatio(frame2)

    # if low grass ratio --> out of field so use correlation only with low threshold
    if frame1_GR < 0.15:
        if corr < 3:
            cuts.append((frame_number, "hard cut"))

    # if high grass ratio --> use both correlation and correlation with higher threshold and grass ratio
    else:
        if corr < 5:
            cuts.append((frame_number, "hard cut"))
           


for Item in cuts:
    print(Item, sep='/n')