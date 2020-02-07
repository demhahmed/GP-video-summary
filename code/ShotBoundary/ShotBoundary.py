import cv2
import numpy as np
import FrameSkipping as ExtractFrames
from HistogramCompare import *
from func import printProgressBar


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
last_frame = (-50, "")
print(len(frames))

for i in range(len(frames)-1):
    frame_number = i*step
    frame1 = frames[i]
    frame2 = frames[i+1]

    intersect, corr = HistogramCompare(frame1, frame2)

    # if intersect < 4 and corr > 9:
    #cuts.append((frame_number, "logo"))
    #last_frame = (frame_number, "logo")
    if corr < 5:
        cuts.append((frame_number, "hard cut"))
        last_frame = (frame_number, "hard cut")


flag = 0
i = 0


for Item in cuts:
    print(Item, sep='/n')

print("-------------------------------------------")

while(i < len(cuts)-1):

    current = cuts[i][0]
    if cuts[i][1] == "hard cut":
        i += 1
        continue
    elif cuts[i][1] == "logo":
        if cuts[i+1][1] != "logo" and cuts[i][0] != flag:
            cuts.pop(i)

        elif cuts[i+1][0] - cuts[i][0] >= cutOffset and cuts[i][0] == flag:
            cuts.insert(i+1, (cuts[i][0]+cutOffset, "hard cut"))
            i += 1
        elif cuts[i+1][1] == "logo" and cuts[i+1][0] - cuts[i][0] <= cutOffset:
            cuts.pop(i+1)
            flag = cuts[i][0]

        else:
            i += 1


i = 0
while(i < len(cuts)-1):
    if cuts[i][1] == "logo" and cuts[i-1][1] == "hard cut" and cuts[i][0]-cuts[i-1][0] <= 10:
        cuts.pop(i-1)
        i -= 1
    else:
        i += 1
