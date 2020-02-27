def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    #####################################

    cap = cv2.VideoCapture('file')

    cap = cv2.VideoCapture('file')


cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

resize(ret, ret, Size(800, 600), 0, 0, INTER_CUBIC)
