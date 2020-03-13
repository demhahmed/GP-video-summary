import cv2
import numpy as np
from FrameSkipping import ExtractFrames
from Audio import get_peak_times
from moviepy.editor import VideoFileClip, concatenate
import bisect
from ShotBoundary import cutDetector
from Utill import blockPrint, enablePrint, printProgressBar, find_gt
from goal_detector import GoalDetector
from classify import ShotClassifier
from os.path import dirname, realpath, join
import math
from goalpostv2 import goalMouth


############################## declarations ##################################
STEP = 5
VIDEO_PATH = 'C://Users\\medo\\Desktop\\test5.mp4'
frames = []
shots = []
mouth = False
cuts = []
skip = 0
type = ''
patch = 0
out = False
cap = cv2.VideoCapture(VIDEO_PATH)
if cap.isOpened() == False:
    print('err reading video')

############################## video info ##################################
FPS = int(cap.get(cv2.CAP_PROP_FPS))
############################## main loop ##################################
while 1:
    frames = []

    count = 0

    while cap.isOpened():
        ret, image = cap.read()

        if count == 2000*5:
            break

        if ret == True:
            if count % STEP == 0:
                frames.append(image)
            count += 1
        else:
            out = True
            break

    print(out)
    last_cut = 0
    No_frames = int(len(frames))
    for i in range(len(frames)-1):
        skip = 0
        frame_number = i*STEP
        printProgressBar(i, No_frames)
        frame1 = frames[i]
        frame2 = frames[i+1]
        mouth = False

        if cutDetector(frame1, frame2) and abs(last_cut - frame_number) >= 20:

            skip = math.ceil(
                len(frames[int(last_cut/STEP):int(frame_number/STEP)])/10)

            type = ShotClassifier(model_type=1).get_shot_class(
                frames[int(last_cut/STEP):int(frame_number/STEP):skip])

            if type not in ['logo', 'close-out', 'close']:
                mouth = goalMouth(
                    frames[int(frame_number/STEP-20):int(frame_number/STEP)])

            shots.append((frame_number, (frame_number/FPS), GoalDetector().execute(
                frames[int(max(last_cut/5 - 2, 0))], frames[i-1]), type, mouth))
            cuts.append(frame_number/FPS)
            last_cut = frame_number
    patch += 1

    if out:
        break
############################## print cuts  ##################################
print("----------------------")
print("Found ", len(shots), " shots")
print("----------------------")

for shot in shots:
    print(shot)


############################## audio processing ##################################
'''
print("Analyzing Audio...")
peak_times = get_peak_times(VIDEO_PATH)
print(peak_times)
'''

############################## removing duplicate cuts ##################################

'''
final_times = []
for peak in peak_times:
    index = find_gt(cuts, peak)
    if cuts[index] < peak:
        final_times.append((cuts[index], cuts[index+1]))
    else:
        final_times.append((cuts[index-1], cuts[index+1]))

final_times = [t for t in (set(tuple(i) for i in final_times))]
print(final_times)
'''

################################## rendering video  ######################################
'''
print("rendering video...")
blockPrint()
clip = VideoFileClip(VIDEO_PATH)
final = concatenate([clip.subclip(max(int(t[0]), 0), min(int(t[1]), clip.duration))
                     for t in final_times])

enablePrint()
final.to_videofile('soccer_cuts.mp4', fps=24)  # low quality is the default
'''
