import cv2
import numpy as np


def ExtractFramesToDisk(path, step):
    cap = cv2.VideoCapture(path)
    if cap.isOpened() == False:
        print('err reading video')

    count = 0
    while cap.isOpened():

        ret, image = cap.read()

        if ret == True:
            if count % step == 0:
                cv2.imwrite(
                    "C:/Users\\salama\\Desktop\\frames\\frame%d.jpg" % count, image)
            count += 1
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    return True


def ExtractFrames(path, step):

    list = []

    cap = cv2.VideoCapture(path)
    if cap.isOpened() == False:
        print('err reading video')

    count = 0

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while cap.isOpened():

        ret, image = cap.read()

        if ret == True:
            if count % step == 0:
                list.append(image)
            count += 1
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    return list


def ExtractFrames(path, step, patch):

    Nframes = patch * 2000
    list = []

    cap = cv2.VideoCapture(path)
    if cap.isOpened() == False:
        print('err reading video')

    count = 0

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while cap.isOpened():

        printProgressBar(count, total)

        ret, image = cap.read()

        if ret == True:
            if count % step == 0:
                list.append(image)
            count += 1
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    return list


vidoe_name = "matchnew5"
VIDEO_PATH = 'C:/Users\\salama\\Desktop\\'+vidoe_name+'.mp4'

#ExtractFramesToDisk(VIDEO_PATH, 5)
