import cv2
import numpy as np
import math  

def compare_intersect(h1, h2):
    result = 0
    
    assert len(h1) == len(h2)
    
    for j in range(len(h1)):
        result += min(h1[j], h2[j])
    return result

def compare_correlation(h1, h2):
    assert len(h1) == len(h2)
    #covariance(X, Y) / (stdv(X) * stdv(Y))
    n = len(h1)
    cov = (sum((h1 - np.mean(h1)) * (h2 - np.mean(h2)) )) * 1/(n-1)

    return cov / (np.std(h1) * np.std(h2))
  
def calc_Hist(img):
    # calculate histogram
    row, col = img.shape
    y = np.zeros((256), np.uint64)
    for i in range(row):
        for j in range(col):
            y[img[i,j]] += 1

    # compress it to 64 values
    result = []
    f = 0
    val = 0
    for i in range(len(y)):
        val += y[i]
        f += 1
        if f == 4:
            f = 0
            result.append(val)
            val = 0
            
    return result

def normalize(arr):
    _sum = 0 
    for i in range(len(arr)):
        _sum += arr[i]**2
    _norm = math.sqrt(_sum)
    
    return np.asarray(arr) / _norm  # normalized array

def histogram_compare(img_1, img_2):
    frame1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)

    hist1 = calc_Hist(frame1)
    hist1 = normalize(hist1)


    hist2 = calc_Hist(frame2)
    hist2 = normalize(hist2)
    
    return compare_intersect(hist1, hist2), 10 * compare_correlation(hist1, hist2)


def block_change(frame1, frame2):
    count = 0
    for r in range(0, frame1.shape[0], 150):
        for c in range(0, frame2.shape[1], 150):
            window1 = frame1[r:r + 150, c:c + 150]
            window2 = frame2[r:r + 150, c:c + 150]
            intersect, corr = histogram_compare(window1, window2)
            if intersect < 4 and corr < 4:
                count += 1
            elif intersect > 4 and corr < 4:
                count += 0.75
            elif intersect > 4 and corr > 4:
                count += 0.25
            elif intersect < 4 and corr > 4:
                count += 0.1
    return (count / 28 * 100)


def cut_detector(frame1, frame2):
    intersect, corr = histogram_compare(frame1, frame2)
    if intersect > 6 and corr > 5:
        return False
    return block_change(frame1, frame2) >= 30