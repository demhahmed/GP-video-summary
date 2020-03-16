from functools import reduce
from GoalMouth.GoalPostV2 import goalMouth
import math
from os.path import dirname, realpath, join
from ShotClassifier.ShotClassifier import ShotClassifier
from GoalDetector.GoalDetector import GoalDetector
from UTL.UTL import *
from ShotBoundary.ShotBoundary import cut_detector
import bisect
from moviepy.editor import VideoFileClip, concatenate
from Audio.Audio import get_peak_times
from Extraction.FrameSkipping import ExtractFrames
from ImageTools.ImageTools import ImageTools
import cv2
import numpy as np



############################## declarations ##################################
STEP = 5                                                         # frame step
VIDEO_PATH = 'C://Users\\medo\\Desktop\\test6.mp4'
frames = []                                                      # patch frames
shots = []                                                       # shot
# shot caontains goal mouth or not
mouth = False
# times of cuts in sec
cuts = []
# skip frames in classification
skip = 0
type = ''                                                       # type of shot
patch = 0                                                    # no pf patch
out = False                                                 # video ended
cap = cv2.VideoCapture(VIDEO_PATH)
if cap.isOpened() == False:
    print('err reading video')

############################## video info ##################################
FPS = int(cap.get(cv2.CAP_PROP_FPS))
############################## main loop ##################################
while 1:  # main loop

    frames = []
    count = 0

    # extracting patch of 2000 frames
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

    # no of last cut
    last_cut = 0
    # no of frames in this patch
    No_frames = int(len(frames))

    # loop on patch frames
    for i in range(No_frames-1):

        skip = 0
        frame_number = i*STEP
        printProgressBar(i, No_frames)
        frame1 = frames[i]
        frame2 = frames[i+1]
        mouth = False
        frames_to_classify = []
        types = []

        # detecting cut between the current 2 frames
        if cutDetector(frame1, frame2) and abs(last_cut - frame_number) >= 20:  # there is a cut

            # appending the first and last 5 frames and 10 random frames inbetween
            if No_frames > 16:

                frames_to_classify.append(frames[0:5])

                skip = math.ceil(
                    len(frames[5:No_frames-5])/10)

                frames_to_classify.append(
                    frames[int(last_cut/STEP):int(frame_number/STEP):skip])

                frames_to_classify.append(frames[-5:])

            else:
                frames_to_classify.append(frames)

            # frames_to_classify.flatten()
            reduce(lambda x, y: x+y, frames_to_classify)

            # getting the shot type
            type = ShotClassifier(model_type=1).get_shot_class(
                frames_to_classify)

            if "+" in type:
                types = type.split("+")
                if types[0] == "logo":
                    shots.append(
                        (frame_number, (frame_number/FPS), False, "logo", False))
                    shots.append(
                        (frame_number+5, (frame_number+5/FPS), False, types[1], False))
                else:
                    shots.append(
                        (frame_number, (frame_number/FPS), False, types[0], False))
                    shots.append(
                        (frame_number+5, (frame_number+5/FPS), False, "logo", False))

            else:
                if type not in ['logo', 'close-out', 'close']:
                    mouth = goalMouth(
                        frames[int(frame_number/STEP-20):int(frame_number/STEP)])

                # appending all shot information
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
############################### adding volume to shots ####################################
'''
audio_binary = []
for i in range(len(shots)):
    for j in range((len(final_times))):
        if final_times[j][0] == shots[i][1]:
            audio_binary.append(1)
        else:
            audio_binary.append(0)
'''
############################# processing output shots #################################
'''
output_video_shots = []
logo_count = 0
for i in range(len(shots)):
    if shots[i][5] == "logo":
        logo_count+=1

    if logo_count == 2:
        j=i
        while(1)
            output_video_shots.append(shots[j])
            if logo_count == 0 and shots[j][5] == "wide":
                break
            j-=1
            logo_count-=1
            
output_video_shots.reverse()
'''
