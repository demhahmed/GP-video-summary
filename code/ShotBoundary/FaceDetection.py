from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
from matplotlib.patches import Rectangle
import cv2

detector = MTCNN()


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

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # RGB color to gray level

    faces = detector.detect_faces(img)
    if len(faces) > 0:
        x, y, width, height = faces[0]['box']
        if width*height > 2000:
            #highlight_faces(img, faces)
            return len(faces)
    return 0
