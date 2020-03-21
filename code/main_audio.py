from Audio.Audio import get_peak_times
from GoalMouth.GoalPostV2 import goalMouth
from ShotBoundary.ShotBoundary import cut_detector
from moviepy.editor import VideoFileClip, concatenate
import cv2
import numpy as np
import time

VIDEO_PATH = 'C:/Users\\salama\\Desktop\\match2.mp4'
clip = VideoFileClip(VIDEO_PATH)
fps = int(clip.fps)
print(fps)
print("Analyzing Audio...")
peak_times = get_peak_times(VIDEO_PATH)
print(peak_times)

patch=1
Frames = []
Final_Video = []
t1 = time.time()

for i in range(len(peak_times)):
    if len(Final_Video) != 0 and peak_times[i] < Final_Video[-1][1]:
        continue
    seconds_1 = 0
    seconds_2 = 0
    while(1):
        cut = cut_detector(clip.get_frame(((peak_times[i]*fps)-seconds_1)/fps),clip.get_frame(((peak_times[i]*fps)-seconds_1-5)/fps))
        if (cut):
            shot_start = ((peak_times[i]*fps)-seconds_1)/fps
            break
        seconds_1 += 5
    if len(Final_Video) != 0 and shot_start < Final_Video[-1][1]:
        continue
    while(1):
        cut = cut_detector(clip.get_frame(((peak_times[i]*fps)+seconds_2)/fps),clip.get_frame(((peak_times[i]*fps)+seconds_2+5)/fps))
        if (cut):
            shot_end = ((peak_times[i]*fps)+seconds_2)/fps
            break
        seconds_2 += 5
    if (shot_end-shot_start > 1):
        print(peak_times[i],shot_start,shot_end) 
        Final_Video.append((shot_start,shot_end))

t2 = time.time()

print(t2-t1)

################################## rendering video  ######################################
print("rendering video...")
final = concatenate([clip.subclip(max(int(t[0]), 0), min(int(t[1]), clip.duration))
                     for t in Final_Video])

final.to_videofile('soccer_cuts.mp4', fps=24)  # low quality is the default

   
          


        
