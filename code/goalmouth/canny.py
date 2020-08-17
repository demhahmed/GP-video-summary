import numpy as np
from scipy import ndimage
import cv2
from scipy.ndimage.filters import convolve

weak_pixel = 50
strong_pixel = 255

def sobel_edge_detection(img):
    sobel_filter_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    sobel_filer_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)

    I_x = ndimage.filters.convolve(img, sobel_filter_x)
    I_y = ndimage.filters.convolve(img, sobel_filer_y)

    G = np.hypot(I_x, I_y)
    G = G / G.max() * 255
    direction = np.arctan2(I_y, I_x)
    return G, direction

def non_max_suppression(mag, direction):
    M, N = mag.shape
    res = np.zeros((M,N), dtype=np.int32)
    angle = direction * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M-1):
        for j in range(1, N-1):

            if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                q = mag[i, j+1]
                r = mag[i, j-1]
            elif (22.5 <= angle[i,j] < 67.5):
                q = mag[i+1, j-1]
                r = mag[i-1, j+1]
            elif (67.5 <= angle[i,j] < 112.5):
                q = mag[i+1, j]
                r = mag[i-1, j]
            elif (112.5 <= angle[i,j] < 157.5):
                q = mag[i-1, j-1]
                r = mag[i+1, j+1]

            if (mag[i,j] >= q) and (mag[i,j] >= r):
                res[i,j] = mag[i,j]

    return res

def threshold(img, low= 50, high= 100):
    res = np.zeros(img.shape)

    strong_row, strong_col = np.where(img >= high)
    weak_row, weak_col = np.where((img <= high) & (img >= low))

    res[strong_row, strong_col] = strong_pixel
    res[weak_row, weak_col] = weak_pixel
    return res

def edge_tracking(img):
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            if (img[i,j] == weak_pixel):
                if ((img[i+1, j-1] == strong_pixel) 
                    or (img[i+1, j] == strong_pixel) 
                    or (img[i+1, j+1] == strong_pixel)
                    or (img[i, j-1] == strong_pixel) 
                    or (img[i, j+1] == strong_pixel)
                    or (img[i-1, j-1] == strong_pixel) 
                    or (img[i-1, j] == strong_pixel) 
                    or (img[i-1, j+1] == strong_pixel)):
                    img[i, j] = strong_pixel
                else:
                    img[i, j] = 0

    return img

def canny_main(img, low, high):
    img = cv2.GaussianBlur(img, (9, 9), 0)
    grad_magnitude, grad_direction = sobel_edge_detection(img)
    img = non_max_suppression(grad_magnitude, grad_direction)
    img = threshold(img, low, high)
    return edge_tracking(img)