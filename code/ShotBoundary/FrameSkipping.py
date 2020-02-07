import cv2


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def ExtractFramesToDisk(path, step):
    # Path to video file
    cap = cv2.VideoCapture(path)
    if cap.isOpened() == False:
        print('err reading video')
    # Used as counter variable
    count = 0
    # checks whether frames were extracted

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
    # Path to video file
    cap = cv2.VideoCapture(path)
    if cap.isOpened() == False:
        print('err reading video')
    # Used as counter variable
    count = 0
    # checks whether frames were extracted
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while cap.isOpened():

        printProgressBar(count, total)
        # vidObj object calls read
        # function extract frames
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


ExtractFramesToDisk('C:/Users\\salama\\Desktop\\test.mp4',6)