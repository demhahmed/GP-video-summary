import numpy as np
from canny import canny_main
import cv2

def image_to_gray(image):
    """ Takes Image with channels b, g, r respectively """
    # Y = 0.2125 R + 0.7154 G + 0.0721 B
    gray_image = image.copy()
    return np.array(0.2125 * gray_image[:, :, 2] + 0.7154 * gray_image[:, :, 1] + 0.0721 * gray_image[:, :, 0])

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


def same(line1, line2):
    if line1[0][0] == line2[0][0] and line1[0][1] == line2[0][1] and line1[0][2] == line2[0][2] and line1[0][3] == line2[0][3]:
        return True
    else:
        return False


def detect(lines):
    for line in lines:
        if (magnitude(*line[0]) < 200):
            # print("YEP")
            continue
        pf = 0
        for lin in lines:
            if (magnitude(*lin[0]) < 200):
                # print("YEP")
                continue
            if same(line, lin):
                # print("YEP")
                continue
            else:
                if isparallel(line, lin):
                    pf += 1
                if pf >= 2:
                    return True
    return False


def goalMouth(frames):
    res = [goalpostv2(x) for x in frames]
    if res.count(True)/len(res) > 0.5:
        return True
    else:
        return False


def goalpostv2(img_rgb):
    img_bgr = img_rgb[..., ::-1]
    gray = image_to_gray(img_bgr)
    #_, bw_img = cv2. threshold(gray, 127, 255, cv2.THRESH_BINARY)
    edges = canny_main(gray)
    #img_goalpost = cv2.medianBlur(edges, 5)
    kernel = np.ones((7, 7))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((5, 5), np.uint8)

    #edges = cv2.dilate(edges, kernel, iterations=1)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 65,
                            minLineLength=40, maxLineGap=10)
    if lines is None:
        # print(False)
        return False
    return detect(lines)