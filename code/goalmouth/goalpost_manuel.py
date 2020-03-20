import numpy as np
from canny import canny_main
import cv2

def image_to_gray(image):
    """ Takes Image with channels b, g, r respectively """
    # Y = 0.2125 R + 0.7154 G + 0.0721 B
    gray_image = image.copy()
    return np.array(0.2125 * gray_image[:, :, 2] + 0.7154 * gray_image[:, :, 1] + 0.0721 * gray_image[:, :, 0])

def magnitude(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2.0 + (y2-y1)**2.0)


def lineangle(line):
    x1, y1, x2, y2 = line[0]
    angle = np.arctan2(y2 - y1, x2 - x1)
    return angle % (2 * np.pi)


def isparallel(line1, line2, tol=None):
    tol = np.pi / (180 * 60 * 60) if tol == None else tol
    angle1 = lineangle(line1) % np.pi
    angle2 = lineangle(line2) % np.pi
    diff = abs(angle1 - angle2)
    diff = min(diff, np.pi - diff)
    return diff < tol


def same(line1, line2):
    if line1[0][0] == line2[0][0] and line1[0][1] == line2[0][1] and line1[0][2] == line2[0][2] and line1[0][3] == line2[0][3]:
        return True
    else:
        return False


def detect(lines):
    for line in lines:
        if (magnitude(*line[0]) < 200):
            # print("YEP")
            continue
        pf = 0
        for lin in lines:
            if (magnitude(*lin[0]) < 200):
                # print("YEP")
                continue
            if same(line, lin):
                # print("YEP")
                continue
            else:
                if isparallel(line, lin):
                    pf += 1
                if pf >= 2:
                    return True
    return False

def hough_line(img, angle_step=1, lines_are_white=True, value_threshold=5):
    # Rho and Theta ranges
    thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
    width, height = img.shape
    diag_len = int(round(math.sqrt(width * width + height * height)))
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2)

    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    num_thetas = len(thetas)

    # Hough accumulator array of theta vs rho
    accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)
    # (row, col) indexes to edges
    are_edges = img > value_threshold if lines_are_white else img < value_threshold
    y_idxs, x_idxs = np.nonzero(are_edges)

    # Vote in the hough accumulator
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]

        for t_idx in range(num_thetas):
            # Calculate rho. diag_len is added for a positive index
            rho = diag_len + int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
            accumulator[rho, t_idx] += 1

    return accumulator

def goalMouth(frames):
    res = [goalpostv2(x) for x in frames]
    if res.count(True)/len(res) > 0.5:
        return True
    else:
        return False

def goalpostv2(img_rgb):
    img_bgr = img_rgb[..., ::-1]
    gray = image_to_gray(img_bgr)
    edges = canny_main(gray)
    accumulator = hough_line(edges)

    # Threshold some high values then draw the line
    edge_pixels = np.where(accumulator > 200)
    coordinates = list(zip(edge_pixels[0], edge_pixels[1]))

    if coordinates is None:
        return False
    lines = []
    # Use line equation to draw detected line on an original image
    for i in range(0, len(coordinates)):
        a = np.cos(np.deg2rad(coordinates[i][1]))
        b = np.sin(np.deg2rad(coordinates[i][1]))
        x0 = a*coordinates[i][0]
        y0 = b*coordinates[i][0]
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        lines.append([x1, y1, x2, y2])

    return detect(lines)