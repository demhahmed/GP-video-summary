import cv2
import numpy as np
from FrameSkipping import ExtractFrames
from Audio import getPeakTimes
from moviepy.editor import VideoFileClip, concatenate
import bisect
from ShotBoundary import cutDetector
from Utill import blockPrint, enablePrint, printProgressBar, find_gt
from goal_detector import GoalDetector
from classify import ShotClassifier
from os.path import dirname, realpath, join


############################## constants ##################################
STEP = 5

############################## reading video ##################################
print("reading video")

VIDEO_PATH = 'C://Users\\medo\\Desktop\\3_1.mp4'

cap = cv2.VideoCapture(VIDEO_PATH)
if cap.isOpened() == False:
    print('err reading video')

############################## video info ##################################
FPS = int(cap.get(cv2.CAP_PROP_FPS))
'''
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))



print(height, width)
'''

############################## extracting frames ##################################
print("extracting frames...")
frames = ExtractFrames(VIDEO_PATH, step=STEP)

print("shot boundary detection...")
shots = []
cuts = []
goals = []
types = []
last_cut = 0
No_frames = int(len(frames))
for i in range(len(frames)-1):
    frame_number = i*STEP
    printProgressBar(i, No_frames)
    frame1 = frames[i]
    frame2 = frames[i+1]

    if cutDetector(frame1, frame2) and abs(last_cut - frame_number) >= 20:

        shots.append((frame_number, (frame_number/FPS), GoalDetector().execute(frames[int(max(last_cut/5 - 2, 0))], frames[i-1]), ShotClassifier(model_type=1).get_shot_class(
            frames[int(last_cut/STEP):int(frame_number/STEP):4])))
        cuts.append((frame_number/FPS))

        last_cut = frame_number


############################## print cuts  ##################################
print("----------------------")
print("Found ", len(shots), " shots")
print("----------------------")

for shot in shots:
    print(shot)


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
