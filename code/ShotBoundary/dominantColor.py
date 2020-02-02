import cv2
# defining channels boundries
HUE_LOWER = 0.15
HUE_UPPER = 0.4
INTENSITY_LOWER = 0.2
INTENSITY_UPPER = 0.6
SATURATION_LOWER = 0.1
SATURATION_UPPER = 1


def equalizeHistColor(frame):
    # equalize the histogram of color image
    img = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)  # convert to HSV
    # equalize the histogram of the V channel
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])
    # convert the HSV image back to RGB format
    return cv2.cvtColor(img, cv2.COLOR_HSV2RGB)


def getDominantColor(frame):
    # converting the middle pannel into HSI
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

    hue = frame[:, :, 0]/255
    intensity = frame[:, :, 1]/255
    saturation = frame[:, :, 2]/255

    frame[(hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (intensity <
                                                                                   INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER)] = 255
    frame[~((hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (
        intensity < INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER))] = 0

    return frame


def getDominantColorRatio(frame):
    # converting the middle pannel into HSI
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

    hue = frame[:, :, 0]/255
    intensity = frame[:, :, 1]/255
    saturation = frame[:, :, 2]/255

    green = (hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (intensity <
                                                                                     INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER)
    frame[(green)] = 255
    frame[~((hue > HUE_LOWER) & (hue < HUE_UPPER) & (intensity > INTENSITY_LOWER) & (
        intensity < INTENSITY_UPPER) & (saturation > SATURATION_LOWER) & (saturation < SATURATION_UPPER))] = 0

    percentage = sum(x.count(255) for x in frame) / \
        (frame.shape[0]*frame.shape[1])
    return percentage


# reading a video
cap = cv2.VideoCapture(
    'C://Users\medo\Desktop\GP REPO\GP-video-summary\code\ShotBoundary\\test3.mp4')

if cap.isOpened() == False:
    print('err reading video')

# getting video width, height and FPS
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))

print(height, width)
# initializing a video writer object
out = cv2.VideoWriter('outpy.mp4', cv2.VideoWriter_fourcc(
    'm', 'p', '4', 'v'), 25, (width, height))
if out.isOpened() == False:
    print('err open video to write')


while cap.isOpened():
    # reading a frame
    ret, frame = cap.read()

    frame = getDominantColor(frame)

    # writing the output video frame by frame
    out.write(frame)

    # displaying the video frame by frame
    if ret == True:
        cv2.imshow('frame', frame)

        if cv2.waitKey(25) == ord('q'):
            break

    else:
        break

# closing all windows
cap.release()
out.release()
cv2.destroyAllWindows()
