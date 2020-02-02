import cv2
import numpy as np
from FrameSkipping import FrameCapture
from FrameBlocks import getFrameBlocks
from FrameBlocks import getDominantColorRatio

frame1 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame850.jpg')
frame2 = cv2.imread(
    'C:/Users\\medo\\Desktop\\frame_test\\frame855.jpg')


frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

# extract a 3D RGB color histogram from the image,
# using 8 bins per channel, normalize, and update
# the index
hist1 = cv2.calcHist([frame1], [0, 1, 2], None, [64, 64, 64],
                     [0, 256, 0, 256, 0, 256])
hist1 = cv2.normalize(hist1, hist1).flatten()


hist2 = cv2.calcHist([frame2], [0, 1, 2], None, [64, 64, 64],
                     [0, 256, 0, 256, 0, 256])
hist2 = cv2.normalize(hist2, hist2).flatten()


OPENCV_METHODS = (
    ("Correlation", cv2.HISTCMP_CORREL),
    ("Chi-Squared", cv2.HISTCMP_CHISQR),
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))


metric_val1 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
metric_val2 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
metric_val3 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
metric_val4 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)

print(metric_val1, metric_val2, metric_val3, metric_val4)
