from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
from matplotlib.patches import Rectangle
import cv2
detector = MTCNN()

img = cv2.imread('C:/Users\\medo\\Desktop\\frame_test\\frame2765.jpg')


def highlight_faces(image, faces):
    # display image

    plt.imshow(image)
    ax = plt.gca()
    # for each face, draw a rectangle based on coordinates
    if len(faces) > 0:
        x, y, width, height = faces[0]['box']
        face_border = Rectangle((x, y), width, height, fill=False, color='red')
        ax.add_patch(face_border)
        plt.show()


def faceDetect(frame):

    faces = detector.detect_faces(frame)
    highlight_faces(img, faces)
    return len(faces)


img = cv2.imread('C:/Users\\medo\\Desktop\\frame_test\\frame11020.jpg')

print(faceDetect(img))
