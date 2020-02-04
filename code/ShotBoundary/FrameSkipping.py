import cv2


def ExtractFramesToDisk(path, step, option):
    # Path to video file
    cap = cv2.VideoCapture(path)
    if cap.isOpened() == False:
        print('err reading video')
    # Used as counter variable
    count = 0
    # checks whether frames were extracted

    while cap.isOpened():
        .

       ret, image = cap.read()

        if ret == True and count % step == 0:
            cv2.imwrite(
                "C:/Users\\medo\\Desktop\\frames\\frame%d.jpg" % count, image)
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

    while cap.isOpened():

        # vidObj object calls read
        # function extract frames
        ret, image = cap.read()

        if ret == True and count % step == 0:
            list.append(image)
            count += 1
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    return list
