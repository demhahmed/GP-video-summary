from ShotBoundary.ShotBoundary import cut_detector
from moviepy.editor import VideoFileClip, concatenate
from Audio.Audio import get_peak_times
import cv2
import numpy as np
import time
############################## declarations ##################################
STEP = 5                                                         # frame step
VIDEO_PATH = 'C:/Users\\salama\\Desktop\\match2.mp4'
frames = []                                                      # patch frames

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
peak_times = get_peak_times(VIDEO_PATH)
print(peak_times)
############################## video info ##################################
FPS = int(cap.get(cv2.CAP_PROP_FPS))
############################## main loop ##################################
t1 = time.time()
while 1:  # main loop
    included_times = [x for x in peak_times if x >= ((patch*2000*5)/FPS) and x<= (((patch*2000*5)+(2000*5))/FPS)]
    if len(included_times) == 0:
        print("patch is empty: ",patch)
        if ((patch*2000*5)/FPS) > peak_times [-1]:
            break
        patch+=1
        continue
        
    cap.set(cv2.CAP_PROP_POS_FRAMES,patch*2000*5)

    frames = []
    count = 0

    print("extracting patch ", patch)
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
    

    for i in range(len(included_times)):
        frame_index_1 = int((included_times[i]*FPS)/5) - (patch*2000)
        frame_index_2 = frame_index_1
        while(1):
            if frame_index_1 == 0:
                shot_start = frame_index_1/FPS*5 + ((patch * 2000 * 5) / FPS)
                break
            if (cut_detector(frames[frame_index_1],frames[frame_index_1-1])):
                shot_start = frame_index_1/FPS*5 + ((patch * 2000 * 5) / FPS)
                break
            frame_index_1 -= 1
        if len(Final_Video) != 0 and not (shot_start > Final_Video[-1][1] -5):
            shot_start = Final_Video[-1][1]
        while(1):
            if frame_index_2 == len(frames) - 1:
               shot_end = frame_index_2/FPS*5 + ((patch * 2000 * 5) / FPS)
               break
            if (cut_detector(frames[frame_index_2],frames[frame_index_2+1])):
                shot_end = frame_index_2/FPS*5 + ((patch * 2000 * 5) / FPS)
                break
            frame_index_2 +=1

        if (shot_end+5 == shot_start):
            continue
        if len(Final_Video) != 0 and not (shot_start > Final_Video[-1][1]):
            shot_start = Final_Video[-1][1]
        Final_Video.append((shot_start,shot_end+5))
        print(included_times[i], shot_start , shot_end+5)
    
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

final.to_videofile('soccer_cuts.mp4', fps=24)  # low quality is the default




