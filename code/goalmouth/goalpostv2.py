import cv2
import numpy as np


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
    if len(frames) <= 0:
        return False
    res = [goalpostv2(x) for x in frames]
    if res.count(True)/len(res) > 0.5:
        return True
    else:

        return False


def goalpostv2(img):
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, bw_img = cv2. threshold(gray, 127, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(gray, 50, 200)
    # img_goalpost = cv2.medianBlur(edges, 5)
    kernel = np.ones((7, 7))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((5, 5), np.uint8)

    # edges = cv2.dilate(edges, kernel, iterations=1)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 65,
                            minLineLength=40, maxLineGap=10)
    del img, gray, edges, kernel
    if lines is None:
        # print(False)
        return False
    return detect(lines)

# pathnames = glob.glob("test-set/*.jpg")
# k = 0
# m = 0
# for pathname in pathnames:
#     img = cv2.imread(pathname, cv2.IMREAD_COLOR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     #_, bw_img = cv2. threshold(gray, 127, 255, cv2.THRESH_BINARY)
#     edges = cv2.Canny(gray, 50, 200)
#     #img_goalpost = cv2.medianBlur(edges, 5)
#     kernel = np.ones((7,7))
#     edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
#     kernel = np.ones((5,5), np.uint8)

#     #edges = cv2.dilate(edges, kernel, iterations=1)
#     cv2.imwrite('preprocess_'+str(m)+'.jpg', edges)
#     m += 1
#     lines = cv2.HoughLinesP(edges, 1, np.pi/180, 65, minLineLength=40, maxLineGap=10)
#     if lines is None:
#         print(pathname, False)
#         continue
#     a,b,c = lines.shape
#     for i in range(a):
#         cv2.line(edges, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (23, 32, 42), 3, cv2.LINE_AA)
#     cv2.imwrite('houghlines_'+str(k)+'.jpg',edges)
#     k += 1
#     print(pathname, detect(lines))


'''
frames = []
count = 2580
while(1):
    frames.append(cv2.imread(
        "C:/Users\\medo\\Desktop\\GP REPO\\GP-video-summary\\code\\GoalMouth\\frame%d.jpg" % count))
    count += 5
    if count == 2675:
        break

print(goalMouth(frames))
'''
