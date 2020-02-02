import cv2
import numpy as np
from FrameSkipping import FrameCapture
from FrameBlocks import getFrameBlocks


path = 'C://Users\medo\Desktop\GP REPO\GP-video-summary\code\ShotBoundary\\test3.mp4'
cap = cv2.VideoCapture(path)

if cap.isOpened() == False:
    print('err reading video')

# getting video width, height and FPS
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))

frames = FrameCapture(path, step=10)

for i in range(len(frames)-1):
    frame1 = frames[i]
    frame2 = frames[i+1]

    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update
    # the index
    hist1 = cv2.calcHist([frame1], [0, 1, 2], None, [50, 50, 50],
                         [0, 256, 0, 256, 0, 256])
    hist1 = cv2.normalize(hist1, hist1).flatten()

    hist2 = cv2.calcHist([frame2], [0, 1, 2], None, [50, 50, 50],
                         [0, 256, 0, 256, 0, 256])
    hist2 = cv2.normalize(hist2, hist2).flatten()

    metric_val1 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
    metric_val2 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)

    print(i*10, metric_val1, metric_val2)

    if i == 240:
        break