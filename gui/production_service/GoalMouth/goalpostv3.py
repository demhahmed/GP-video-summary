import cv2
import numpy as np

grass_color = (100,150,50)
grass_color_threshold = 20

goalpost_color = (220,220,220)
goalpost_color_threshold = 5

median_kernel_size = 5
morph_close_kernel_size = 7

def cieluv(img, target):
    img = img.astype('int')
    aR, aG, aB = img[:,:,0], img[:,:,1], img[:,:,2]
    bR, bG, bB = target
    rmean = ((aR + bR) / 2).astype('int')
    r2 = np.square(aR - bR)
    g2 = np.square(aG - bG)
    b2 = np.square(aB - bB)
    result = (((512+rmean)*r2)>>8) + 4*g2 + (((767-rmean)*b2)>>8)
    result = result.astype('float64')
    result -= result.min()
    result /= result.max()
    result *= 255
    result = result.astype('uint8')

    return result

def magnitude(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2.0 + (y2-y1)**2.0)


def lineangle(line):
    x1, y1, x2, y2 = line[0]
    angle = np.arctan2(y2 - y1, x2 - x1)
    return angle % (2 * np.pi)


def isparallel(line1, line2, tol=None):
    tol = np.pi / (180 * 60 * 60) if tol == None else tol
    angle1 = lineangle(line1) % np.pi
    angle2 = lineangle(line2) % np.pi
    diff = abs(angle1 - angle2)
    diff = min(diff, np.pi - diff)
    return diff < tol

def detect(edges, T1, T2, T3, T4):
    #65, 40, 10                           75, 60, 30 for wide
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, T2, minLineLength=T3, maxLineGap=T4)
    if lines is None:
        return False
    #
    #  

    for i in range(len(lines)):
        if (magnitude(*lines[i][0]) < T1):
            # print("YEP")
            continue
        pf = 0
        for j in range(i + 1, len(lines)):
            if (magnitude(*lines[j][0]) < T1):
                # print("YEP")
                continue
            if isparallel(lines[i], lines[j]):
                pf += 1
            if pf >= 2:
                return True
    return False


def goalpostv3(img, T1, T2, T3, T4):
    # remove grass color
    grass = cieluv(img, grass_color) < grass_color_threshold
    img.flags.writeable = True
    img[grass] = [0,0,0]
    
    # extract goalpost color
    goalpost = cieluv(img, goalpost_color) < goalpost_color_threshold
    img_goalpost = goalpost.astype(bool).astype('uint8') * 255

    # clean goalpost image
    img_goalpost = cv2.medianBlur(img_goalpost, 5)
    kernel = np.ones((morph_close_kernel_size,morph_close_kernel_size),np.uint8)
    img_goalpost = cv2.morphologyEx(img_goalpost, cv2.MORPH_CLOSE, kernel)
    
    # compute image density
    density = img_goalpost.mean()/255

    if density < 0.3: # 0.3
        # detect lines
        return detect(img_goalpost, T1, T2, T3, T4)
    else:
        return False 


def goalMouth(frames, type):
    if len(frames) <= 0:
        return False
    T1 = 200 
    T2 = 65
    T3 = 40
    T4 = 10
    if type == "wide":
        T1 = 1
        T2 = 75
        T3 = 60
        T4 = 30
    res = [goalpostv3(x, T1, T2, T3, T4) for x in frames]
    if res.count(True)/len(res) > 0.5:
        return True
    else:

        return False