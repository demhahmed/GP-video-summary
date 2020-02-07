import cv2
import numpy as np


OPENCV_METHODS = (
    ("Correlation", cv2.HISTCMP_CORREL),
    ("Chi-Squared", cv2.HISTCMP_CHISQR),
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))


# option =1  for intersection and correlation
# option =2  for all metrics

def histogramCompare(frame1, frame2):

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

    metrics = []

    metrics.append(cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT))
    metrics.append(10*cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL))

    return metrics
