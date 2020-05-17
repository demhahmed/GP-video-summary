import cv2
import numpy as np

def compare_intersect(h1, h2):
    result = 0
    
    if len(h1) != len(h2):
        print(False)
        return
    
    for j in range(len(h1)):
        result += min(h1[j], h2[j])
    return result

def compare_correlation(h1, h2):
    if len(h1) != len(h2):
        print(False)
        return
    return np.corrcoef(h1, h2)[0][1]
    

def histogram_compare(image_1, image_2):
    
    frame1 = image_1[..., ::-1]
    frame2 = image_2[..., ::-1]
    
    hist1 = cv2.calcHist([frame1], [0, 1, 2], None, [
                         64, 64, 64], [0, 256, 0, 256, 0, 256])

    #hist, bins = np.histogram(image_1.ravel(), 64, [0,256])


    hist1 = cv2.normalize(hist1, hist1).flatten()

    hist2 = cv2.calcHist([frame2], [0, 1, 2], None, [
                         64, 64, 64], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.normalize(hist2, hist2).flatten()
    
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