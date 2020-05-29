import cv2
import numpy as np
import math

# paper 1

def lineangle(line):
    x1, y1, x2, y2 = line[0]
    angle = np.arctan2(y2 - y1, x2 - x1)
    return angle % (2 * np.pi)

def degree(x):
    return math.degrees(x)

def isparallel_wide(line1, line2, tol=2):
    angle1 = lineangle(line1) % np.pi
    angle2 = lineangle(line2) % np.pi
    angle1 = degree(angle1)
    angle2 = degree(angle2)
    diff = abs(angle1 - angle2)
    return diff < tol

def detect_wide(lines):
    for i in range(len(lines)):
        an = lineangle(lines[i])
        an = degree(an)
        if (10 < an and an < 40) or (140 < an and an < 170):
            pf = 0
            for j in range(i + 1, len(lines)):
                an = lineangle(lines[i])
                an = degree(an)
                if (10 < an and an < 40) or (140 < an and an < 170):
                    if isparallel_wide(lines[i], lines[j]):
                        pf += 1
                    if pf >= 2:
                    	del lines
                    	return True
    del lines
    return False

def wide(im):
    # optional
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    im = cv2.GaussianBlur(im, (5, 5), 0)
    #
    edges = cv2.Canny(im, 60, 120)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 90, minLineLength=80, maxLineGap=10)

    del edges
    if lines is None:
        return False
    
    return detect_wide(lines)

# paper 2

def prep(img1, img2):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

    light, dark = (36, 25, 25), (70, 255, 255)
    
    hsv = cv2.cvtColor(img1, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, light, dark)

    final_result = cv2.bitwise_and(img2, img2, mask=mask)

    del mask, hsv
    return final_result

def magnitude(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2.0 + (y2-y1)**2.0)

def isparallel_medium(line1, line2, tol=None):
    tol = np.pi / (180 * 60 * 60) if tol == None else tol
    angle1 = lineangle(line1) % np.pi
    angle2 = lineangle(line2) % np.pi
    diff = abs(angle1 - angle2)
    diff = min(diff, np.pi - diff)
    return diff < tol

def detect_medium(edges):
    # 65, 50, (5) or 7 or 8        // 75 60 10                 
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 75, minLineLength=60, maxLineGap=10) # maxline can be 5 or 8
    
    del edges

    if lines is None:
        return False

    for i in range(len(lines)):
        # if (magnitude(*lines[i][0]) < 1):
        #     continue
        pf = 0
        for j in range(i + 1, len(lines)):
            # if (magnitude(*lines[j][0]) < 1):
            #     continue
            if isparallel_medium(lines[i], lines[j]):
                pf += 1
            if pf >= 2:
            	del lines
            	return True
    del lines
    return False

def medium(img):
    im = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    im = cv2.GaussianBlur(im, (5, 5), 0)
    
    img_goalpost = cv2.Canny(im, 50, 100) # 50 100
    edges = prep(img, img_goalpost)

    return detect_medium(edges)


def goalMouth(frames, type):
    if len(frames) <= 0:
        return False

    if type == "wide":
        res = [wide(x) for x in frames]
    else:
        res = [medium(x) for x in frames]

    if res.count(True)/len(res) > 0.5:
        return True
    else:

        return False
