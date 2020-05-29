from Audio.audio import get_peak_times
from UTL.UTL import find_gt, blockPrint, enablePrint,  printProgressBar
import time
import operator
from moviepy.editor import VideoFileClip, concatenate_videoclips
from ShotClassifier.ShotClassifier import ShotClassifier
from GoalDetector.GoalDetector import GoalDetector
from GoalMouth.goalpostv4 import goalMouth
import math
from os.path import dirname, realpath, join
from ShotBoundary.ShotBoundary import cut_detector
from ImageTools.ImageTools import ImageTools
import cv2
import numpy as np
import gc
from UTL.classes import shot
import subprocess
import glob
from pymongo import MongoClient
from bson.objectid import ObjectId

# 0.9 for step 1
# 0.1 for step 8

current_progress = 0

# connect to database
client = MongoClient(port=27017)
db = client.la5asly

def STEP_1_shots_processing(cap, SHOT_TYPES, summary_id, coefficient):
    model = ShotClassifier(model_type=1)
    goal_detector = GoalDetector()
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    STEP = 5
    # VARIABLE DECLARATIONS _____________________________________________
    frames, frame_times, frame_numbers, shots, frames_to_classify, types = [], [], [], [], [], []
    patch, last_cut_frame_number, No_frames = 0, 0, 0
    mouth, out = False, False
    PATCH_FRAMES = 10000  # 2000 * 5
    type = ''
    total_number_of_patches = cap.get(cv2.CAP_PROP_FRAME_COUNT) // 10000
    current_patch = 0
    # MAIN LOOP  _______________________________________________________
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
                current_patch += 1
                current_progress = int(coefficient * (current_patch / total_number_of_patches) * 100)
                db.summaries.find_one_and_update({"_id": ObjectId(summary_id)}, {"$set": { "progress": current_progress } })
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

        # loop on patch frames
        for i in range(No_frames-1):

            printProgressBar(i, No_frames-1)

            frame1, frame2 = frames[i], frames[i+1]

            frame_number = frame_numbers[i]
            frame_time = frame_times[i]

            # detecting cut between the current 2 frame

            # last_cut_frame_number => to delete shot < 20 frames

            if (cut_detector(frame1, frame2) and abs(last_cut_frame_number - frame_number) >= 20):

                no_shot_frames = 0
                mouth = False
                frames_to_classify.clear()
                types.clear()

                gc.collect()

                no_shot_frames = len(frames[start:i+1])

                # appending the first and last 5 frames and 10 random frames inbetween
                frames_to_classify += frames[start:i+1] if no_shot_frames <= 20 else frames[start:start+5] + \
                    frames[start + 5: i-4: math.ceil(
                        len(frames[start+5:i-4])/10)] + frames[i - 4:i+1]

                # getting the shot type

                type = model.get_shot_class(frames_to_classify)

                if "+" not in type:

                    if type not in [SHOT_TYPES.LOGO, SHOT_TYPES.CLOSE_OUT, SHOT_TYPES.CLOSE]:
                        mouth = goalMouth(frames[i-20:i], type)

                # appending all shot information
                    shots.append(shot(frame_number=frame_number,
                                      shot_start=round(frame_times[start], 2),
                                      shot_end=round((frame_times[i]), 2),
                                      type=type,
                                      has_goal=goal_detector.execute(
                                          frames[int(max(start - 2, 0))], frames[i-2]),
                                      has_goal_mouth=mouth))

                    last_cut_frame_number = frame_number

                else:
                    types = type.split("+")
                    if types[0] == SHOT_TYPES.LOGO:
                        shots.append(shot(frame_number=last_cut_frame_number+25,
                                          shot_start=round(
                                              frame_times[start], 2),
                                          shot_end=round(
                                              frame_times[start] + (25/FPS), 2),
                                          type=SHOT_TYPES.LOGO))

                        if types[1] not in [SHOT_TYPES.LOGO, SHOT_TYPES.CLOSE_OUT, SHOT_TYPES.CLOSE]:
                            mouth = goalMouth(frames[i-20:i], types[1])

                        shots.append(shot(frame_number=frame_number,
                                          shot_start=round(
                                              frame_times[start] + (25/FPS), 2),
                                          shot_end=round(frame_time, 2),
                                          type=types[1],
                                          has_goal_mouth=mouth))
                        last_cut_frame_number = frame_number

                    else:
                        if types[0] not in [SHOT_TYPES.LOGO, SHOT_TYPES.CLOSE_OUT, SHOT_TYPES.CLOSE]:
                            mouth = goalMouth(frames[i-25:i-5], types[0])

                        shots.append(shot(frame_number=frame_number-25,
                                          shot_start=round(
                                              frame_times[start], 2),
                                          shot_end=round(
                                              ((frame_time-(25/FPS))), 2),
                                          type=types[0],
                                          has_goal_mouth=mouth))

                        shots.append(shot(frame_number=frame_number,
                                          shot_start=round(
                                              ((frame_time-(25/FPS))), 2),
                                          shot_end=round(frame_time, 2),
                                          type=SHOT_TYPES.LOGO))

                        last_cut_frame_number = frame_number

                start = i + 1

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

    del frames_to_classify, patch, mouth, out, type, no_shot_frames, frames
    gc.collect()

    return shots


def STEP_2_resolving_double_logos(shots, SHOT_TYPES):
    i = 0
    while i <= len(shots)-2:
        if shots[i].type == SHOT_TYPES.LOGO and shots[i+1].type == SHOT_TYPES.LOGO:
            shots.pop(i+1)
            i -= 1
        i += 1


def STEP_3_audio_processing(shots, VIDEO_PATH, summary_id):
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

    for i in range(len(shots)):
        for j in range((len(final_times))):
            if final_times[j][1] == shots[i].shot_end:
                shots[i].audio = True
                break




def STEP_4_processing_output_shots(shots, SHOT_TYPES, summary_id):
    output_video_shots_1, output_video_shots_2 = [], []
    logo_count = 0
    time_after_first_logo = 0
    for i in range(len(shots)):
        if shots[i].type == SHOT_TYPES.LOGO:
            logo_count += 1
        if logo_count == 1:
            time_after_first_logo += shots[i].shot_end - shots[i].shot_start
            if time_after_first_logo > 60:
                logo_count = 0
                time_after_first_logo = 0

        if logo_count == 2:
            time_after_first_logo = 0
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

    output_video_shots_1.sort(key=lambda x: x.frame_number)
    # shots with high volume but not replayed
    for i in range(len(shots)):
        if shots[i].audio and shots[i] not in output_video_shots_1:
            if shots[i].type == SHOT_TYPES.WIDE and shots[i].shot_end - shots[i].shot_start > 10:
                shots[i].shot_start = shots[i].shot_end - 10
            output_video_shots_2.append(shots[i])


    return output_video_shots_1, output_video_shots_2


def STEP_5_classifying_shot_sequence(output_video_shots_1, output_video_shots_2, SHOT_TYPES, EVENT_TYPES, summary_id):
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
                                  time.strftime("%H:%M:%S", time.gmtime(output_video_shots_2[i].shot_end)), "attack"))
        else:
            shots_classes.append((output_video_shots_2[i].frame_number, time.strftime("%H:%M:%S", time.gmtime(output_video_shots_2[i].shot_start)),
                                  time.strftime("%H:%M:%S", time.gmtime(output_video_shots_2[i].shot_end)), "other"))



    return shots_classes


def STEP_6_processing_final_output(output_video_shots_1, output_video_shots_2, shots_classes, SHOT_TYPES):
    output_video_shots = output_video_shots_1 + output_video_shots_2
    output_video_shots.sort(key=lambda x: x.frame_number)
    final_video = []  # final video for render
    for i in range(len(output_video_shots)):
        time_between_shots = output_video_shots[i].shot_end - \
            output_video_shots[i].shot_start
        if output_video_shots[i].type == SHOT_TYPES.WIDE and time_between_shots > 10:
            final_video.append(
                (output_video_shots[i].shot_end - 10, output_video_shots[i].shot_end))
        else:
            final_video.append(
                (output_video_shots[i].shot_start, output_video_shots[i].shot_end))

    for i in range(len(output_video_shots)):
        output_video_shots[i].shot_start = time.strftime(
            "%H:%M:%S", time.gmtime(output_video_shots[i].shot_start))
        output_video_shots[i].shot_end = time.strftime(
            "%H:%M:%S", time.gmtime(output_video_shots[i].shot_end))
    shots_classes.sort(key=operator.itemgetter(0))

    return output_video_shots, final_video


def STEP_7_file_output(shots_classes, EVENT_TYPES, video_name, shots, output_video_shots, output_video_shots_2, t1, t2, summary_id):
    GOAL_count, ATTACK_count, OTHER_count = 0, 0, 0

    for shot_class in shots_classes:
        if shot_class[3] == EVENT_TYPES.GOAL:
            GOAL_count += 1
        if shot_class[3] == EVENT_TYPES.ATTACK:
            ATTACK_count += 1
        if shot_class[3] == EVENT_TYPES.OTHER:
            OTHER_count += 1

    f = open("{0}.txt".format(video_name), "w")
    f.write("Video Shots: {0}".format(str(len(shots)))+"\n\n")

    for i in range(len(shots)):
        try:
            shots[i].shot_start = time.strftime(
                "%H:%M:%S", time.gmtime(shots[i].shot_start))
            shots[i].shot_end = time.strftime(
                "%H:%M:%S", time.gmtime(shots[i].shot_end))
            f.write(str(shots[i]))
        except:
            f.write(str(shots[i]))

    f.write("\nno. of shots come from audio: {0} \n\n" .format(
            str(len(output_video_shots_2))))
    f.write(str(output_video_shots_2))
    f.write("\n\nImportant Events: {0}\n\n".format(len(output_video_shots)))
    f.write(str(output_video_shots))
    f.write("\n\nGOALS: {0} | ATTACKS: {1} | OTHER: {2} ".format(str(GOAL_count),
                                                                 str(ATTACK_count), str(OTHER_count)))

    f.write("\n\nSHOT CLASSES\n")
    for tup in shots_classes:
        f.write(f"#{tup[0]} start: {tup[1]}, end: {tup[2]}, class: {tup[3]}\n")

    f.write("\n\nrunning time: {0}".format(str(t2-t1)))
    f.close()

    result = db.summaries.find_one({"_id": ObjectId(summary_id)})
    for object_id in result["versions"]:
        summary_version = db.summaryversions.find_one({"_id": ObjectId(object_id)})
        if summary_version["type"] == "detailed":
            summary_version["goals"] = GOAL_count
            summary_version["chances"] = ATTACK_count
            summary_version["others"] = OTHER_count
            db.summaryversions.save(summary_version)
            break


def STEP_8_rendering_video(final_video, VIDEO_PATH, output_file_path, summary_id):
    print("rendering video...")
    optimized = []
    for start, end in final_video:
        if len(optimized) > 0:
            if abs(int(start) - optimized[-1][1]) <= 10:
                optimized[-1][1] = int(end)
            else:
                optimized.append([int(start), int(end)])
        else:
            optimized.append([int(start), int(end)])
    cnt = 1
    folder_name = str(int(time.time()))
    subprocess.run(["mkdir", folder_name])

    for start, end in optimized:
        subprocess.run(["ffmpeg", "-ss", str(start), "-i", VIDEO_PATH,
                        "-c", "copy", "-t", str(end - start), f"{folder_name}/{cnt}.mp4"])
        cnt += 1
    filenames = glob.glob(f"{folder_name}/*.mp4")
    filenames.sort(key=lambda filename: int(
        filename.split(".")[0].split("/")[1]))
    with open(f"{folder_name}.txt", mode="w") as file:
        for path in filenames:
            file.write(f"file {path}\n")
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i",
                    f"{folder_name}.txt", "-c", "copy", f"{output_file_path}"])
    subprocess.run(["rm", "-r", f"{folder_name}"])
    subprocess.run(["rm", f"{folder_name}.txt"])
    db.summaries.find_one_and_update({"_id": ObjectId(summary_id)}, {"$set": { "progress": current_progress + 10 } })
    print("done")