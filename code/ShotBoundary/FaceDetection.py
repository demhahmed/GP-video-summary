
from cv2 import rectangle
from cv2 import CascadeClassifier
from cv2 import destroyAllWindows
from cv2 import waitKey
from cv2 import imshow
from cv2 import imread

cascPath = 'C:/Users\\medo\\Desktop\\GP REPO\\GP-video-summary\\code\\ShotBoundary\\haarcascade_frontalface_default.xml'


def faceDetection(pixels):
    classifier = CascadeClassifier(cascPath)
    bboxes = classifier.detectMultiScale(pixels)
    if len(bboxes) > 0:
        return True
