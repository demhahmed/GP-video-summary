import cv2
import numpy as np
from FrameSkipping import FrameCapture
from FrameBlocks import getFrameBlocks
from FrameBlocks import getDominantColorRatio


OPENCV_METHODS = (
    ("Correlation", cv2.HISTCMP_CORREL),
    ("Chi-Squared", cv2.HISTCMP_CHISQR),
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))


def HistogramCompareAll(frame1, frame2, method):
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

    metrics1 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
    metrics2 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
    metrics3 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    metrics4 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    return metrics1, metrics2, metrics3, metrics4


 def HistogramCompareOne(frame1, frame2, method):
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


    metric=cv2.compareHist(hist1, hist2,method)
    return metric
  


  def HistogramCompare(frame1, frame2):
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


    metric1=cv2.compareHist(hist1, hist2,cv2.HISTCMP_INTERSECT)
    metric2=cv2.compareHist(hist1, hist2,cv2.HISTCMP_CORREL)
    return metric1,metric2
  
    





