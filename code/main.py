
from GoalMouth.goalpostv2 import goalMouth, goalpostv2
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


def main():
    ############################## declarations #################################
    VIDEO_PATH = 'C://Users\\medo\\Desktop\\test5.mp4'
    cap = cv2.VideoCapture(VIDEO_PATH)
    if cap.isOpened() == False:
        print('err reading video')
    FPS = int(cap.get(cv2.CAP_PROP_FPS))

    STEP = 5
    frames, shots, frames_to_classify, types = [], [], [], []
    skip, patch, start = 0, 0, 0
    mouth, out = False, False
    type = ''                                                       # type of shot
    ############################## main loop ##################################
    while 1:  # main loop
        p = patch*2000
        frames.clear()
        # append frames from after last cut
        count = 0

        print("extracting patch ", patch, '\n')
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

        last_cut = 0
        No_frames = int(len(frames))

        # loop on patch frames
        for i in range(No_frames-1):

            printProgressBar(i, No_frames)

            frame1, frame2 = frames[i], frames[i+1]
            frame_number = i*STEP

            # detecting cut between the current 2 frames
            if cut_detector(frame1, frame2) and abs(last_cut - frame_number) >= 20:

                no_shot_frames, skip = 0
                mouth = False
                frames_to_classify.clear()
                types.clear()
                frame_time = (frame_number)/FPS
                no_shot_frames = len(frames[start:i])

                # appending the first and last 5 frames and 10 random frames inbetween
                frames_to_classify += frames[start:i] if no_shot_frames < 20 else frames[start:start+5] + \
                    frames[start + 5: i-5: math.ceil(
                        len(frames[start+5:i-5])/10)] + frames[i - 5:i]

                # getting the shot type
                type = ShotClassifier(model_type=1).get_shot_class(
                    frames_to_classify)

                if "+" not in type:

                    if type not in ['logo', 'close-out', 'close']:
                        mouth = goalMouth(frames[i-20:i])

                # appending all shot information
                    shots.append((frame_number+(p*5), frame_time,
                                  GoalDetector().execute(
                                      frames[int(max(start - 2, 0))],
                                      frames[i-2]), type, mouth, False))

                else:
                    types = type.split("+")
                    if types[0] == "logo":
                        shots.append(
                            (frame_number+(p*5), frame_time, False, "logo", False, False))
                        if types[1] not in ['logo', 'close-out', 'close']:
                            mouth = goalMouth(frames[i-20:i])
                        shots.append(
                            (frame_number+5+(p*5), frame_time+5/FPS, False, types[1], mouth, False))

                    else:
                        if types[0] not in ['logo', 'close-out', 'close']:
                            mouth = goalMouth(frames[i-25:i-5])
                        shots.append(
                            (frame_number+(p*5), frame_time, False, types[0], mouth, False))
                        shots.append((frame_number+5+(p*5), frame_time+(5/FPS),
                                      False, "logo", False, False))
                    del types
                last_cut = frame_number
                start = i
        patch += 1

        if out:
            break

    frames.clear()
    del frames, frames_to_classify, skip, patch, mouth, out, type, no_shot_frames
    ############################## audio processing ##################################

    print("Analyzing Audio...")
    peak_times = get_peak_times(VIDEO_PATH)
    print(peak_times)

    cuts = [x[1] for x in shots]
    final_times = []
    for peak in peak_times:
        index = find_gt(cuts, peak)
        if cuts[index] < peak:
            final_times.append((cuts[index], cuts[index+1]))
        else:
            final_times.append((cuts[index-1], cuts[index]))

    final_times = [t for t in (set(tuple(i) for i in final_times))]

    print("final ", final_times)
    ############################## print cuts  ##################################
    print("----------------------")
    print("Found ", len(shots), " shots")
    print("----------------------")

    for i in range(len(shots)):
        for j in range((len(final_times))):
            if final_times[j][1] == shots[i][1]:
                shots[i] = (shots[i][0], shots[i][1], shots[i]
                            [2], shots[i][3], shots[i][4], True)
                break

    for shot in shots:
        print(shot)

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


main()
