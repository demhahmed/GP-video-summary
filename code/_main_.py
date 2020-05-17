
from GoalMouth.goalpostv4 import goalMouth
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
import operator


class shot:
    def __init__(self, frame_number, shot_time, type=None, has_goal=None, has_goal_mouth=None, audio=None):
        self.frame_number = frame_number
        self.shot_time = shot_time
        self.type = type if type is not None else False
        self.has_goal = has_goal if has_goal is not None else False
        self.has_goal_mouth = has_goal_mouth if has_goal_mouth is not None else False
        self.audio = audio if audio is not None else []

    def __repr__(self):
        return str(self)

    def __str__(self):
        shot_info = "frame_number: " + str(self.frame_number)+"| "+"time: " + str(self.shot_time)+"| "+"type: " + str(
            self.type)+"| "+"goal: " + str(self.has_goal)+"| "+"goal_mouth: "+str(self.has_goal_mouth)+"| "+"high_volume: "+str(self.audio)+"\n"
        return shot_info


def main():
    # declarations___________________________________________________________________________
    vidoe_name = "test12--"
    VIDEO_PATH = 'C:/Users\\medo\\Desktop\\video test\\'+vidoe_name+'.mkv'
    cap = cv2.VideoCapture(VIDEO_PATH)
    if cap.isOpened() == False:
        print('err reading video')
        return

    STEP = 5
    FPS = int(cap.get(cv2.CAP_PROP_FPS))

    last_frames, shots, frames_to_classify, types = [], [], [], []
    frames, frame_times, frame_numbers = [], [], []
    skip, patch, last_cut_frame_number = 0, 0, 0
    mouth, out = False, False
    type = ''
    # main loop ##################################
    while(1):

        frames, frame_times, frame_numbers = [], [], []

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
            if (cut_detector(frame1, frame2) and abs(last_cut_frame_number - frame_number) >= 20):

                no_shot_frames = 0
                skip = 0
                mouth = False
                frames_to_classify.clear()
                types.clear()

                no_shot_frames = len(frames[start:i+1])

                # appending the first and last 5 frames and 10 random frames inbetween
                frames_to_classify += frames[start:i+1] if no_shot_frames < 20 else frames[start:start+5] + \
                    frames[start + 5: i-4: math.ceil(
                        len(frames[start+5:i-4])/10)] + frames[i - 4:i+1]

                # getting the shot type
                type = ShotClassifier(model_type=1).get_shot_class(
                    frames_to_classify)

                if "+" not in type:

                    if type not in ['logo', 'close-out', 'close']:
                        mouth = goalMouth(frames[i-20:i], type)

                # appending all shot information
                    shots.append(shot(frame_number=frame_numbers[i],
                                      shot_time=round((frame_times[i]/60), 2),
                                      type=type,
                                      has_goal=GoalDetector().execute(
                                          frames[int(max(start - 2, 0))], frames[i-2]),
                                      has_goal_mouth=mouth,
                                      audio=False))
                    last_cut_frame_number = frame_numbers[i]

                else:
                    types = type.split("+")
                    if types[0] == "logo":
                        shots.append(shot(frame_number=last_cut+25+(p*5),
                                          shot_time=round(
                                              (((last_cut+25)/FPS)/60), 2),
                                          type="logo",
                                          has_goal=False,
                                          has_goal_mouth=False,
                                          audio=False))

                        if types[1] not in ['logo', 'close-out', 'close']:
                            mouth = goalMouth(frames[i-20:i], types[1])

                        shots.append(shot(frame_number=frame_number+(p*5),
                                          shot_time=round((frame_time/60), 2),
                                          type=types[1],
                                          has_goal=False,
                                          has_goal_mouth=mouth,
                                          audio=False))
                        last_cut_frame_number = frame_number+(p*5)

                    else:
                        if types[0] not in ['logo', 'close-out', 'close']:
                            mouth = goalMouth(frames[i-25:i-5], types[0])

                        shots.append(shot(frame_number=frame_number-25+(p*5),
                                          shot_time=round(
                                              ((frame_time-(25/FPS))/60), 2),
                                          type=types[0],
                                          has_goal=False,
                                          has_goal_mouth=mouth,
                                          audio=False))

                        shots.append(shot(frame_number=frame_number+(p*5),
                                          shot_time=round((frame_time/60), 2),
                                          type="logo",
                                          has_goal=False,
                                          has_goal_mouth=False,
                                          audio=False))
                        last_cut_frame_number = frame_number+(p*5)

                last_cut = frame_number
                start = i+1
        patch += 1

        if out:
            break

        last_frames = frames[start:]
        last_frame_times = frame_times[start:]
        last_frame_numbers = frame_numbers[start:]
        del frames, frame_times, frame_numbers
        frames, frame_times, frame_numbers = [], [], []
        frames = frames+last_frames
        frame_times = frame_times+last_frame_times
        frame_numbers = frame_numbers+last_frame_numbers
        del last_frames, last_frame_times, last_frame_numbers

    type = ShotClassifier(model_type=1).get_shot_class(
        frames[::int(len(frames)/10)])
    # appending last shot in video
    shots.append(shot(frame_number=frame_numbers[-1],
                      shot_time=round((frame_times[-1]/60), 2),
                      type=type,
                      has_goal=GoalDetector().execute(
        frames[start-3], frames[start+3]),
        has_goal_mouth=goalMouth(frames[::int(len(frames)/10)], type),
        audio=False))

    del frames_to_classify, skip, patch, mouth, out, type, no_shot_frames
    ############################### resolving double logos ###########################
    i = 0
    while i <= len(shots)-2:
        if shots[i].type == "logo" and shots[i+1].type == "logo":
            shots.pop(i+1)
            i -= 1
        i += 1
    ############################## audio processing ##################################

    print("Analyzing Audio...")
    peak_times = get_peak_times(VIDEO_PATH, 90)
    peak_times = [x/60 for x in peak_times]

    ############################## Extracting high volume shots #########################
    cuts = [x.shot_time for x in shots]
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

    # Detecing if shot contains high volume
    for i in range(len(shots)):
        for j in range((len(final_times))):
            if final_times[j][1] == shots[i].shot_time:
                shots[i] = shot(shots[i].frame_number, shots[i].shot_time,
                                shots[i].type, shots[i].has_goal, shots[i].has_goal_mouth, True)
                break

    ############################ print shots info into a file #############################
    f = open(vidoe_name+"output.txt", "w")
    for i in range(len(shots)):
        f.write(str(shots[i]))
    f.close()
    ############################# processing output shots #################################
    # main shots depending on replay
    output_video_shots_1, output_video_shots_2 = [], []
    logo_count = 0
    for i in range(len(shots)):
        if shots[i].type == "logo":
            logo_count += 1

        if logo_count == 2:
            j = i
            while(1):
                output_video_shots_1.append(shots[j])
                if logo_count == 0 and shots[j].type == "wide":
                    break

                if shots[j].type == "logo":
                    logo_count -= 1

                j -= 1
    # shots with high volume but not replayed
    for i in range(len(shots)):
        if shots[i].audio == True and shots[i] not in output_video_shots_1:
            output_video_shots_2.append(shots[i])

    output_video_shots_1.sort(key=lambda x: x.frame_number)
    output_video_shots_2.sort(key=lambda x: x.frame_number)
    print(str(output_video_shots_1))
    print(str(output_video_shots_2))

    ################################## classifying shots #####################################
    shots_classes = []
    goal_detected, goal_post, logo_count = 0, 0, 0

    for i in range(len(output_video_shots_1)):
        if output_video_shots_1[i].has_goal == 1 and logo_count == 0:
            goal_detected = 1
        if output_video_shots_1[i].has_goal_mouth == 1 and logo_count == 0:
            goal_post = 1
        if output_video_shots_1[i].audio == 1 and logo_count == 0:
            high_volume = 1
        if output_video_shots_1[i].type == "logo":
            logo_count += 1

        if logo_count != 0 and logo_count % 2 == 0:
            if goal_detected == 1:
                shots_classes.append(
                    (output_video_shots_1[i].frame_number, "GOAL"))
            elif goal_post == 1:
                shots_classes.append(
                    (output_video_shots_1[i].frame_number, "ATTACK"))
            else:
                shots_classes.append(
                    (output_video_shots_1[i].frame_number, "OTHER"))

            goal_detected, goal_post, logo_count = 0, 0, 0

    for i in range(len(output_video_shots_2)):
        if output_video_shots_2[i].has_goal_mouth:
            shots_classes.append(
                (output_video_shots_2[i].frame_number, "ATTACK"))
        else:
            shots_classes.append(
                (output_video_shots_2[i].frame_number, "OTHER"))

    output_video_shots = output_video_shots_1 + output_video_shots_2

    output_video_shots.sort(key=lambda x: x.frame_number)
    shots_classes.sort(key=operator.itemgetter(0))

    print(str(output_video_shots))
    print(shots_classes)
    return

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