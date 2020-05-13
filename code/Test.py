
'''
import cv2
from ShotClassifier.ShotClassifier import ShotClassifier



frames = []
count = 1740
while(1):
    frames.append(cv2.imread(
        "C:/Users\\salama\\Desktop\\GP-video-summary\\code\\frame%d.jpg" % count))
    count += 5
    if count == 1800:
        break

print( ShotClassifier(model_type=1).get_shot_class(
                    frames))


'''

arr = [0,1,2,3,4,5]

print(arr[0:-1])
