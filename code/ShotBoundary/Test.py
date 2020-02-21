import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *

from HistogramCompare import *
from dominantColor import *
from ShotClassification import *


path = 'C:/Users\\medo\\Desktop\\test2.mp4'
cap = cv2.VideoCapture(path)

if cap.isOpened() == False:
    print('err reading video')


# getting video width, height and FPS
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))
print(FPS)

f = open("ntayg.txt", "w")

print("extracting frames...")
frames = ExtractFrames(path, step=5)


for i, frame in enumerate(frames):
    type = ''
    print(i)
    grassRatio = getDominantColorRatio(frame)

    if grassRatio < 0.2:
        type = 'out'
    else:
        faces = faceDetect(frame)
        if grassRatio > 0.65 and faces == 0:
            type = 'long'
        elif grassRatio > 0.4 and faces != 0:
            type = 'close'
    result1 = str(i*5) + ' ' + str(round(grassRatio, 2))+" " + \
        str(faces) + " " + type + "\n"
    f.write(result1)
