from GoalMouth.goalpostv4 import goalMouth
import math
from ShotClassifier.ShotClassifier import ShotClassifier
from GoalDetector.GoalDetector import GoalDetector
from UTL.UTL import printProgressBar, find_gt
from UTL.classes import *
from ShotBoundary.ShotBoundary import cut_detector
from moviepy.editor import VideoFileClip, concatenate
from Audio.audio import get_peak_times
from ImageTools.ImageTools import ImageTools
import cv2
import numpy as np
import operator
import time
import objgraph
import gc


def main():
    # CONSTANTS _________________________________________________________
    video_name = "Arsenal-Chelsea 1 pt1"
    VIDEO_PATH = "{0}{1}{2}".format(
        'C:/Users\\medo\\Desktop\\match_test\\', video_name, '.mp4')
    cap = cv2.VideoCapture(VIDEO_PATH)
    if cap.isOpened() == False:
        print('err reading video')
        return
    model = ShotClassifier(model_type=1)
    goal_detector = GoalDetector()
    SHOT_TYPES = shot_types()
    EVENT_TYPES = event_types()
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    STEP = 5
    # VARIABLE DECLARATIONS _____________________________________________
    frames, frame_times, frame_numbers, shots, frames_to_classify, types = [], [], [], [], [], []
    skip, patch, last_cut_frame_number, No_frames = 0, 0, 0, 0
    mouth, out = False, False
    PATCH_FRAMES = 10000  # 2000*5
    type = ''
    # MAIN LOOP  _______________________________________________________
    t1 = time.time()
    while(1):
        # append frames from after last cut
        count = 0
        start = 0
        print("extracting patch ", patch, '\n')
        offset = patch*PATCH_FRAMES

        # extracting patch of 2000 frames
        while cap.isOpened():
            ret, image = cap.read()

            if count == PATCH_FRAMES:
                No_frames = 2000
                break

            if ret:
                if count % STEP == 0:
                    frames.append(image)
                    frame_times.append(
                        round(cap.get(cv2.CAP_PROP_POS_MSEC)/1000, 1))
                    frame_numbers.append(count+offset)
                count += 1
            else:
                out = True
                No_frames = int(len(frames))
                break

        last_cut = 0

        # loop on patch frames
        for i in range(No_frames-1):

            printProgressBar(i, No_frames-1)

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

                gc.collect()

                no_shot_frames = len(frames[start:i+1])

                # appending the first and last 5 frames and 10 random frames inbetween
                frames_to_classify += frames[start:i+1] if no_shot_frames < 20 else frames[start:start+5] + \
                    frames[start + 5: i-4: math.ceil(
                        len(frames[start+5:i-4])/10)] + frames[i - 4:i+1]

                # getting the shot type

                type = model.get_shot_class(frames_to_classify)

                if "+" not in type:

                    if type not in [SHOT_TYPES.LOGO, SHOT_TYPES.CLOSE_OUT, SHOT_TYPES.CLOSE]:
                        mouth = goalMouth(frames[i-20:i], type)

                # appending all shot information
                    shots.append(shot(frame_number=frame_numbers[i],
                                      shot_start=round(frame_times[start], 2),
                                      shot_end=round((frame_times[i]), 2),
                                      type=type,
                                      has_goal=goal_detector.execute(
                                          frames[int(max(start - 2, 0))], frames[i-2]),
                                      has_goal_mouth=mouth))

                    last_cut_frame_number = frame_numbers[i]

                else:
                    types = type.split("+")
                    if types[0] == SHOT_TYPES.LOGO:
                        shots.append(shot(frame_number=last_cut+25+(offset),
                                          shot_start=round(
                                              frame_times[start], 2),
                                          shot_end=round(
                                              (((last_cut+25)/FPS)), 2),
                                          type=SHOT_TYPES.LOGO))

                        if types[1] not in [SHOT_TYPES.LOGO, SHOT_TYPES.CLOSE_OUT, SHOT_TYPES.CLOSE]:
                            mouth = goalMouth(frames[i-20:i], types[1])

                        shots.append(shot(frame_number=frame_number+(offset),
                                          shot_start=round(
                                              ((last_cut+25)/FPS), 2),
                                          shot_end=round((frame_times[i]), 2),
                                          type=types[1],
                                          has_goal_mouth=mouth))
                        last_cut_frame_number = frame_number+(offset)

                    else:
                        if types[0] not in [SHOT_TYPES.LOGO, SHOT_TYPES.CLOSE_OUT, SHOT_TYPES.CLOSE]:
                            mouth = goalMouth(frames[i-25:i-5], types[0])

                        shots.append(shot(frame_number=frame_number-25+(offset),
                                          shot_start=round(
                                              frame_times[start], 2),
                                          shot_end=round(
                                              ((frame_time-(25/FPS))), 2),
                                          type=types[0],
                                          has_goal_mouth=mouth))

                        shots.append(shot(frame_number=frame_number+(offset),
                                          shot_start=round(
                                              ((frame_time-(25/FPS))), 2),
                                          shot_end=round((frame_time), 2),
                                          type=SHOT_TYPES.LOGO))
                        last_cut_frame_number = frame_number+(offset)

                last_cut = frame_number
                start = i+1

        patch += 1

        if out:
            break

        frames = frames[start:]
        frame_times = frame_times[start:]
        frame_numbers = frame_numbers[start:]
        gc.collect()

    type = model.get_shot_class(
        frames[::int(len(frames)/10)])
    # appending last shot in video
    shots.append(shot(frame_number=frame_numbers[-1],
                      shot_start=round(frame_times[start], 2),
                      shot_end=round((frame_times[-1]), 2),
                      type=type,
                      has_goal=goal_detector.execute(
        frames[start-3], frames[start+3]),
        has_goal_mouth=goalMouth(frames[::int(len(frames)/10)], type)))

    del frames_to_classify, skip, patch, mouth, out, type, no_shot_frames, frames
    gc.collect()
    # resolving double logos _____________________________________________
    i = 0
    while i <= len(shots)-2:
        if shots[i].type == SHOT_TYPES.LOGO and shots[i+1].type == SHOT_TYPES.LOGO:
            shots.pop(i+1)
            i -= 1
        i += 1
    # audio processing _________________________________________________
    print("Analyzing Audio...")
    peak_times = get_peak_times(VIDEO_PATH, 92)

    # Extracting high volume shots ____________________________________
    cuts = [x.shot_end for x in shots]
    final_times = []
    for peak in peak_times:
        index = find_gt(cuts, peak)
        if index != -1:
            if cuts[index] < peak:
                final_times.append((cuts[index], cuts[index+1]))
            else:
                final_times.append((cuts[index-1], cuts[index]))

    final_times = [t for t in (set(tuple(i) for i in final_times))]
    # print cuts  _____________________________________________________
    print("----------------------")
    print("Found ", len(shots), " shots")
    print("----------------------")

    # Detecing if shot contains high volume ____________________________
    for i in range(len(shots)):
        for j in range((len(final_times))):
            if final_times[j][1] == shots[i].shot_end:
                shots[i].audio = True
                break

    # processing output shots __________________________________________________
    # main shots depending on replay
    output_video_shots_1, output_video_shots_2 = [], []
    logo_count = 0
    for i in range(len(shots)):
        if shots[i].type == SHOT_TYPES.LOGO:
            logo_count += 1

        if logo_count == 2:
            j = i
            while(1):
                output_video_shots_1.append(shots[j])
                if logo_count == 0 and (shots[j].type == SHOT_TYPES.WIDE or j == 0 or shots[j].type == SHOT_TYPES.LOGO):
                    if output_video_shots_1[-1].type == SHOT_TYPES.LOGO:
                        output_video_shots_1.pop(-1)
                    break

                if shots[j].type == SHOT_TYPES.LOGO:
                    logo_count -= 1

                j -= 1
    # shots with high volume but not replayed
    for i in range(len(shots)):
        if shots[i].audio and shots[i] not in output_video_shots_1:
            output_video_shots_2.append(shots[i])

    # classifying shots Sequence _____________________________________________
    shots_classes = []
    goal_detected, goal_post, logo_count = 0, 0, 0

    for i in range(len(output_video_shots_1)):
        if output_video_shots_1[i].has_goal and logo_count == 0:
            goal_detected = 1
        if output_video_shots_1[i].has_goal_mouth:
            goal_post = 1
        if output_video_shots_1[i].type == SHOT_TYPES.LOGO:
            logo_count += 1

        if logo_count == 2:
            if goal_detected == 1:
                shots_classes.append((output_video_shots_1[i].frame_number, time.strftime("%H:%M:%S", time.gmtime(output_video_shots_1[i].shot_start)),
                                      time.strftime("%H:%M:%S", time.gmtime(output_video_shots_1[i].shot_end)), EVENT_TYPES.GOAL))
            elif goal_post == 1:
                shots_classes.append((output_video_shots_1[i].frame_number, time.strftime("%H:%M:%S", time.gmtime(output_video_shots_1[i].shot_start)),
                                      time.strftime("%H:%M:%S", time.gmtime(output_video_shots_1[i].shot_end)), EVENT_TYPES.ATTACK))
            else:
                shots_classes.append((output_video_shots_1[i].frame_number, time.strftime("%H:%M:%S", time.gmtime(output_video_shots_1[i].shot_start)),
                                      time.strftime("%H:%M:%S", time.gmtime(output_video_shots_1[i].shot_end)), EVENT_TYPES.OTHER))

            goal_detected, goal_post, logo_count = 0, 0, 0

    for i in range(len(output_video_shots_2)):
        if output_video_shots_2[i].has_goal_mouth:
            shots_classes.append((output_video_shots_2[i].frame_number, time.strftime("%H:%M:%S", time.gmtime(output_video_shots_2[i].shot_start)),
                                  time.strftime("%H:%M:%S", time.gmtime(output_video_shots_2[i].shot_end)), "ATTACK"))
        else:
            shots_classes.append((output_video_shots_2[i].frame_number, time.strftime("%H:%M:%S", time.gmtime(output_video_shots_2[i].shot_start)),
                                  time.strftime("%H:%M:%S", time.gmtime(output_video_shots_2[i].shot_end)), "OTHER"))

    output_video_shots = output_video_shots_1 + output_video_shots_2
    output_video_shots.sort(key=lambda x: x.frame_number)
    final_video = []  # final video for render
    for i in range(len(output_video_shots)):
        final_video.append(
            (output_video_shots[i].shot_start, output_video_shots[i].shot_end))

    for i in range(len(output_video_shots)):
        output_video_shots[i].shot_start = time.strftime(
            "%H:%M:%S", time.gmtime(output_video_shots[i].shot_start))
        output_video_shots[i].shot_end = time.strftime(
            "%H:%M:%S", time.gmtime(output_video_shots[i].shot_end))
    shots_classes.sort(key=operator.itemgetter(0))
    objgraph.show_most_common_types()

    t2 = time.time()

    GOAL_count, ATTACK_count, OTHER_count = 0, 0, 0

    for shot_class in shots_classes:
        if shot_class[3] == EVENT_TYPES.GOAL:
            GOAL_count += 1
        if shot_class[3] == EVENT_TYPES.ATTACK:
            ATTACK_count += 1
        if shot_class[3] == EVENT_TYPES.OTHER:
            OTHER_count += 1

    # write outputs to file ________________________________________________
    f = open("{0}.txt".format(video_name), "w")
    f.write("Video Shots: {0}".format(str(len(shots)))+"\n\n")
    for i in range(len(shots)):
        f.write(str(shots[i]))

    f.write("\nno. of shots come from audio: {0} \n\n" .format(
            str(len(output_video_shots_2))))
    f.write(str(output_video_shots_2))
    f.write("\n\nImportant Events: {0}\n\n".format(len(output_video_shots)))
    f.write(str(output_video_shots))
    f.write("\n\nGOALS: {0} | ATTACKS: {1} | OTHER: {2} ".format(str(GOAL_count),
                                                                 str(ATTACK_count), str(OTHER_count)))

    f.write("\n\nrunning time: {0}".format(str(t2-t1)))
    f.close()

    '''
    # rendering video  _______________________________________________________

    print("rendering video...")
    blockPrint()
    clip = VideoFileClip(VIDEO_PATH)
    final = concatenate([clip.subclip(max(int(t[0]), 0), min(int(t[1]), clip.duration))
                        for t in final_video])

    enablePrint()
    final.to_videofile('soccer_cuts.mp4', fps=24)  # low quality is the default
    '''


main()
