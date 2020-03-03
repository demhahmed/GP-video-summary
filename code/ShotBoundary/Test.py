

import cv2
import image_slicer


a = cv2.imread('C:/Users\\medo\\Desktop\\frames\\frame0.jpg')
b = cv2.imread(
    'C:/Users\\medo\\Desktop\\frames\\frame1.jpg')
image_slicer.slice(a, 28)
