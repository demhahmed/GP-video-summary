
from GoalMouth.goalpostv2 import goalMouth, goalpostv2
import math
from os.path import dirname, realpath, join
from ShotClassifier.ShotClassifier import ShotClassifier
from GoalDetector.GoalDetector import GoalDetector
from UTL.UTL import *
from ShotBoundary.ShotBoundary import cut_detector
import bisect
from moviepy.editor import VideoFileClip, concatenate
from Audio.audio import get_peak_times
from ImageTools.ImageTools import ImageTools
import cv2
import numpy as np


def main():
    ############################## declarations #################################
    VIDEO_PATH = 'C:/Users\\medo\\Desktop\\video test\\test10.mp4'
    cap = cv2.VideoCapture(VIDEO_PATH)
    if cap.isOpened() == False:
        print('err reading video')
    FPS = int(cap.get(cv2.CAP_PROP_FPS))

    STEP = 5
    frames, frame_times, frame_numbers, shots, frames_to_classify, types = [], [], [], [], [], []
    skip, patch = 0, 0
    mouth, out = False, False
    type = ''                                                       # type of shot
    ############################## main loop ##################################
    while(1):  # main loop
        # append frames from after last cut
        count = 0
        start = 0
        print("extracting patch ", patch, '\n')
        p = patch*2000
        # extracting patch of 2000 frames
        while cap.isOpened():
            ret, image = cap.read()

            if count == 2000*5:
                break

            if ret == True:
                if count % STEP == 0:
                    frames.append(image)
                    frame_times.append(
                        round(cap.get(cv2.CAP_PROP_POS_MSEC)/1000, 1))
                    frame_numbers.append(count+patch*2000*5)
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

            frame_number = frame_numbers[i]
            frame_time = frame_times[i]
            # detecting cut between the current 2 frame
            if (cut_detector(frame1, frame2) and abs(last_cut - frame_number) >= 20):

                no_shot_frames = 0
                skip = 0
                mouth = False
                frames_to_classify.clear()
                types.clear()

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
                    shots.append((frame_numbers[i], round((frame_times[i]/60), 2),
                                  GoalDetector().execute(
                                      frames[int(max(start - 2, 0))],
                                      frames[i-2]), type, mouth, False))

                else:
                    types = type.split("+")
                    if types[0] == "logo":
                        shots.append(
                            (last_cut+25+(p*5), round((((last_cut+25)/FPS)/60), 2), False, "logo", False, False))
                        if types[1] not in ['logo', 'close-out', 'close']:
                            mouth = goalMouth(frames[i-20:i])
                        shots.append(
                            (frame_number+(p*5), round((frame_time/60), 2), False, types[1], mouth, False))

                    else:
                        if types[0] not in ['logo', 'close-out', 'close']:
                            mouth = goalMouth(frames[i-25:i-5])
                        shots.append(
                            (frame_number-25+(p*5), round(((frame_time-(25/FPS))/60), 2), False, types[0], mouth, False))
                        shots.append((frame_number+(p*5), round((frame_time/60), 2),
                                      False, "logo", False, False))

                last_cut = frame_number
                start = i
        patch += 1

        if out:
            break
        frames = frames[start:]
        frame_times = frame_times[start:]
        frame_numbers = frame_numbers[start:]

    # appending last shot in video
    shots.append((frame_numbers[-1], round((frame_times[-1]/60), 2), GoalDetector().execute(frames[start-2],
                                                                                            frames[start+2]), ShotClassifier(model_type=1).get_shot_class(frames[::int(len(frames)/10)]), goalMouth(frames[::int(len(frames)/10)]), False))
    del frames_to_classify, skip, patch, mouth, out, type, no_shot_frames
    ############################### resolving double logos ###########################
    i = 0
    while i <= len(shots)-2:
        if shots[i][3] == "logo" and shots[i+1][3] == "logo":
            shots.pop(i+1)
            i -= 1
        i += 1
    ############################## audio processing ##################################

    print("Analyzing Audio...")
    peak_times = get_peak_times(VIDEO_PATH, 90)
    peak_times = [x/60 for x in peak_times]
    cuts = [x[1] for x in shots]
    final_times = []
    for peak in peak_times:
        index = find_gt(cuts, peak)
        if index != -1:
            if cuts[index] < peak:
                final_times.append((cuts[index], cuts[index+1]))
            else:
                final_times.append((cuts[index-1], cuts[index]))

    final_times = [t for t in (set(tuple(i) for i in final_times))]

    print("final peak times ", final_times)
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

    f = open("output.txt", "w")
    for i in range(len(shots)):
        f.write(str(shots[i][0])+" "+str(shots[i][1])+" "+str(shots[i][2]) +
                " "+str(shots[i][3])+" "+str(shots[i][4])+" "+str(shots[i][5])+'\n')
    f.close()
    ############################# processing output shots #################################

    output_video_shots = []
    logo_count = 0
    for i in range(len(shots)):
        if shots[i][3] == "logo":
            logo_count += 1

        if logo_count == 2:
            j = i
            while(1):
                output_video_shots.append(shots[j])
                if logo_count == 0 and shots[j][3] == "wide":
                    break

                if shots[j][3] == "logo":
                    logo_count -= 1

                j -= 1

    output_video_shots.reverse()
    print(output_video_shots)
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
