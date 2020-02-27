import cv2
import numpy as np
from FrameSkipping import *
from FrameBlocks import *
from HistogramCompare import *
from DominantColor import *
from Audio import *
from moviepy.editor import VideoFileClip, concatenate
import bisect
from ShotBoundary import cutDetector
from Utill import *


############################## constants ##################################
STEP = 5

############################## reading video ##################################
print("reading video")

VIDEO_PATH = 'C://Users\\medo\\Desktop\\test1.mp4'

cap = cv2.VideoCapture(VIDEO_PATH)
if cap.isOpened() == False:
    print('err reading video')

############################## video info ##################################
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))


############################## extracting frames ##################################
print("extracting frames...")
frames = ExtractFrames(VIDEO_PATH, step=STEP)


############################## shot boundary ##################################
print("shot boundary detection...")
cuts = []
last_cut = 0
No_frames = int(len(frames))
for i in range(len(frames)-1):
    frame_number = i*STEP
    printProgressBar(i, No_frames)
    frame1 = frames[i]
    frame2 = frames[i+1]

    if cutDetector(frame1, frame2) and abs(last_cut - frame_number) >= 20:
        cuts.append((frame_number/FPS))
        last_cut = frame_number


############################## print cuts  ##################################
print("----------------------")
print("Found ", len(cuts), " cuts")
print("----------------------")
for Item in cuts:
    print(Item, sep='/n')


############################## audio processing ##################################
print("Analyzing Audio...")
peak_times = getPeakTimes(VIDEO_PATH)
print(peak_times)


############################## removing duplicate cuts ##################################

final_times = []
for peak in peak_times:
    index = find_gt(cuts, peak)
    if cuts[index] < peak:
        final_times.append((cuts[index], cuts[index+1]))
    else:
        final_times.append((cuts[index-1], cuts[index+1]))

final_times = [t for t in (set(tuple(i) for i in final_times))]
print(final_times)


################################## rendering video  ######################################
print("rendering video...")
blockPrint()
clip = VideoFileClip(VIDEO_PATH)
final = concatenate([clip.subclip(max(int(t[0]), 0), min(int(t[1]), clip.duration))
                     for t in final_times])

enablePrint()
final.to_videofile('soccer_cuts.mp4', fps=24)  # low quality is the default
