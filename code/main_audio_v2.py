from ShotBoundary.ShotBoundary import cut_detector
from moviepy.editor import VideoFileClip, concatenate
from Audio.Audio import get_peak_times
import cv2
import numpy as np
import time
############################## declarations ##################################
STEP = 5                                                         # frame step
VIDEO_PATH = 'C://Users\\medo\\Desktop\\1.mp4'
frames, frame_times, Final_Video = [], [], []
# no pf patch
patch, shot_start, shot_end = 0, 0, 0
out = False
SIX_MINUTES = 6*60

cap = cv2.VideoCapture(VIDEO_PATH)
if cap.isOpened() == False:
    print('err reading video')

FPS = int(cap.get(cv2.CAP_PROP_FPS))
############################## audio processing ##################################
print("Analyzing Audio...")
peak_times = get_peak_times(VIDEO_PATH)
peak_times = np.array(peak_times)

############################## main loop ##################################
t1 = time.time()
while 1:  # main loop

    current_time = (SIX_MINUTES)*patch
    next_time = ((patch+1)*SIX_MINUTES)

    if len(peak_times) == 0:
        break
    included_times = [x for x in peak_times if x >
                      current_time and x < next_time]

    peak_times = [x for x in peak_times if x not in included_times]

    print(included_times, peak_times)

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
        if count == SIX_MINUTES*FPS:
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

    while(len(included_times)):
        '''
        t3 = time.time()

        frame_index_1 = (np.abs(frame_times-included_times[0])).argmin()
        frame_index_2 = frame_index_1
        cut_time = included_times.pop(0)
        print("time", time.time() - t3)
        '''

        t3 = time.time()
        given_value = included_times[0]

        def absolute_difference_function(
            list_value): return abs(list_value - given_value)
        frame_index_1 = frame_times.index(
            min(frame_times, key=absolute_difference_function))
        frame_index_2 = frame_index_1

        cut_time = included_times.pop(0)
        print("time", time.time() - t3)

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
clip = VideoFileClip(VIDEO_PATH)
final = concatenate([clip.subclip(max(int(t[0]), 0), min(int(t[1]), clip.duration))
                     for t in Final_Video])
final.to_videofile('soccer_cuts.mp4', fps=FPS)  # low quality is the default