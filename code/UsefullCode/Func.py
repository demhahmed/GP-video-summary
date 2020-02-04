
import cv2
##################################################
# Program To Read video
# and Extract Frames


def FrameCapture(path):

    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1

    while success:

        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()

        # Saves the frames with frame-count
        cv2.imwrite("frame%d.jpg" % count, image)

        count += 1


##############################################################
# saving video
fileName = 'output.avi'  # change the file name if needed
imgSize = (640, 480)
frame_per_second = 30.0
writer = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc(
    *"MJPG"), frame_per_second, imgSize)

cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        writer.write(frame)                   # save the frame into video file
        cv2.imshow('Video Capture', frame)     # show on the screen
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
    else:
        break

# Release everything if job is finished
cap.release()
writer.release()
cv2.destroyAllWindows()
#########################################################
# loading and saving video
fileName = 'output.avi'  # change the file name if needed

cap = cv2.VideoCapture(fileName)          # load the video
while(cap.isOpened()):                    # play the video by reading frame by frame
    ret, frame = cap.read()
    if ret == True:
        # optional: do some image processing here

        cv2.imshow('frame', frame)              # show the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
####################################################
# color transformations
img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR color to RGB
img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # RGB color to BGR
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # BGR color to gray level
img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # RGB color to gray level
img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   # BGR color to HSV
img = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)   # RGB color to HSV
img = cv2.cvtColor(frame, cv2.COLOR_RGB2HLS)   # RGB color to HLS
img = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)   # BGR color to HLS
# RGB color to CIE XYZ.Rec 709
img = cv2.cvtColor(frame, cv2.COLOR_BGR2XYZ)
# RGB color to CIE XYZ.Rec 709
img = cv2.cvtColor(frame, cv2.COLOR_RGB2XYZ)
img = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)   # BGR color to CIE L\*a\*b\*
img = cv2.cvtColor(frame, cv2.COLOR_RGB2Luv)   # RGB color to CIE L\*u\*v\
##########################################################


def equalizeHistColor(frame):
        # equalize the histogram of color image
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)  # convert to HSV
        # equalize the histogram of the V channel
        img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])
        # convert the HSV image back to RGB format
        return cv2.cvtColor(img, cv2.COLOR_HSV2RGB)


######################################################
frame = cv2.GaussianBlur(frame, (kernelSize, kernelSize), 0, 0)
frame = cv2.Canny(frame, parameter1, parameter2, intApertureSize)
############################################################


def histogram_intersection(h1, h2):
    sm = 0
    for i in range(13):
        sm += min(h1[i], h2[i])
    return sm
