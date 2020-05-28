from ShotBoundary.ShotBoundary import cut_detector
from moviepy.editor import VideoFileClip, concatenate
from Audio.audio import get_peak_times
import cv2
import numpy as np
import time
import sys
import glob
import subprocess
############################## declarations ##################################


def main():
    STEP = 5
    # frame step
    match = sys.argv[2]
    VIDEO_PATH = match + ".mp4"
    frames = []
    # patch frames
    frame_times = []
    patch = 0                                                    # no pf patch
    out = False
    shot_start = 0
    shot_end = 0
    Final_Video = []
    cap = cv2.VideoCapture(VIDEO_PATH)
    if cap.isOpened() == False:
        print('err reading video')
    ############################## audio processing ##################################
    print("Analyzing Audio...")
    peak_times = get_peak_times(VIDEO_PATH, int(sys.argv[1]))
    print(peak_times)
    ############################## video info ##################################
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    ############################## main loop ##################################
    t1 = time.time()
    while 1:  # main loop
        current_time = (6*60)*patch
        next_time = ((patch+1)*6*60)
        if len(peak_times) == 0:
            break
        included_times = [x for x in peak_times if x >=
                          current_time and x < next_time]
        peak_times = [x for x in peak_times if x not in included_times]

        if len(included_times) == 0:
            print("patch is empty: ", patch)
            patch += 1
            continue

        cap.set(cv2.CAP_PROP_POS_FRAMES, (current_time * FPS))

        frames.clear()
        frame_times.clear()
        count = 0

        print("extracting patch ", patch)
        # extracting patch of 2000 frames
        while cap.isOpened():
            if count == 6*60*FPS:
                break
            ret, image = cap.read()
            if ret == True:
                if count % STEP == 0:
                    frames.append(image)
                    frame_times.append(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)

                count += 1
            else:
                out = True
                break
        print(len(frames))
        i = 0
        while(len(included_times)):
            given_value = included_times[i]
            def absolute_difference_function(
                list_value): return abs(list_value - given_value)
            frame_index_1 = frame_times.index(
                min(frame_times, key=absolute_difference_function))
            frame_index_2 = frame_index_1
            cut_time = included_times.pop(i)
            while(1):
                if frame_index_1 == 0:
                    shot_start = frame_times[frame_index_1]
                    break
                if (cut_detector(frames[frame_index_1], frames[frame_index_1-1])):
                    shot_start = frame_times[frame_index_1]
                    break
                frame_index_1 -= 1

            if len(Final_Video) != 0 and not (shot_start > Final_Video[-1][1]):
                shot_start = Final_Video[-1][1]

            while(1):
                if frame_index_2 == len(frames) - 1:
                    shot_end = frame_times[frame_index_2]
                    break
                if (cut_detector(frames[frame_index_2], frames[frame_index_2+1])):
                    shot_end = frame_times[frame_index_2]
                    break
                frame_index_2 += 1

            if (shot_end == shot_start):
                continue

            Final_Video.append((shot_start, shot_end))
            included_times = [x for x in included_times if not (
                x >= shot_start and x <= shot_end)]
            print(cut_time, shot_start, shot_end)

        patch += 1

        if out:
            break

    t2 = time.time()
    print(t2-t1)
    ################################## rendering video  ######################################
    print("rendering video...")

    folder_name = str(int(time.time()))
    subprocess.run(["mkdir", folder_name])
    cnt = 1
    for start, end in Final_Video:
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
                    f"{folder_name}.txt", "-c", "copy", f"{folder_name}/ffmpeg_out.mp4"])
    for path in filenames:
        subprocess.run(["rm", path])
    subprocess.run(["rm", f"{folder_name}.txt"])


if __name__ == "__main__":
    main()
