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

    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HLS)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HLS)

    frame1_blocks = getFrameBlocks(frame1, height, width)
    frame2_blocks = getFrameBlocks(frame2, height, width)
    '''
    cv2.imshow("frame1", cv2.absdiff(frame1_blocks[6], frame2_blocks[6]))

    while True:
        if cv2.waitKey(25) == ord('q'):
            break
    '''
    block_change = [cv2.absdiff(x, y)
                    for x, y in zip(frame1_blocks, frame2_blocks)]

    block_change_average = [np.mean(x) for x in block_change]

    print(np.mean(block_change_average))

    break
