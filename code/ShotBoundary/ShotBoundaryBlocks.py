import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *

from HistogramCompare import *
from dominantColor import *


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


print("reading video")
path = 'C://Users\medo\Desktop\\test4.mp4'
cap = cv2.VideoCapture(path)

if cap.isOpened() == False:
    print('err reading video')


# getting video width, height and FPS
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))


print("extracting frames...")
frames = ExtractFrames(path, step=5)

step = 5
cuts = []
cutOffset = 50
last_frame = (-50, "")
No_frames = int(len(frames))

print(No_frames, "frames")
print("processing...")
for i in range(len(frames)-1):

    frame_number = i*step

    printProgressBar(i, No_frames)

    frame1 = frames[i]
    frame2 = frames[i+1]

    intersect, corr = histogramCompare(frame1, frame2)

    if intersect > 6 and corr > 5:
        continue

    frame_blocks_1 = getFrameBlocks(frame1, height, width)
    frame_blocks_2 = getFrameBlocks(frame2, height, width)

    if blockChangePercentage(frame_blocks_1, frame_blocks_2) >= 30 and abs(last_frame[0] - frame_number) >= 15:
        cuts.append((frame_number, "hard cut"))
        last_frame = (frame_number, "hard cut")


print("----------------------")
print(len(cuts), "cuts")
print("----------------------")
for Item in cuts:
    print(Item, sep='/n')
