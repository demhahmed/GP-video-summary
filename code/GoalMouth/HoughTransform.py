import cv2
import numpy as np


def hough_transform(edges):
    (w, h) = edges.shape
    theta = np.linspace(-90.0, 0.0, np.ceil(90.0) + 1.0)
    theta = np.concatenate((theta, -theta[len(theta) - 2::-1]))

    D = np.sqrt((w - 1) ** 2 + (h - 1) ** 2)
    q = np.ceil(D)
    rho = np.linspace(-q, q, 2 * q + 1)
    accumulator = np.zeros((len(rho), len(theta)))
    for i in range(w):
        for j in range(h):
            if edges[i, j] > 0:
                for t in range(len(theta)):
                    rhoVal = j * np.cos(theta[t] * np.pi / 180.0) + i \
                        * np.sin(theta[t] * np.pi / 180)
                    r = np.nonzero(np.abs(rho - rhoVal)
                                   == np.min(np.abs(rho - rhoVal)))[0]
                    accumulator[r[0], t] += 1
    return (rho, theta, accumulator)


def peak_values(
    accumulator,
    rhos,
    thetas,
    n,
    ):
    flatten = list(set(np.hstack(accumulator)))
    _sorted = sorted(flatten, key=lambda n: -n)
    coords = [np.argwhere(accumulator == val) for val in _sorted[0:n]]
    rhotheta = []
    for idx in range(0, len(coords)):
        allcoords = coords[idx]
        for i in range(0, len(allcoords)):
            (n, m) = allcoords[i]
            rhotheta.append([rhos[n], thetas[m]])
    return rhotheta[0:n]


def check_point(point, ymax, xmax):
    (x, y) = point
    if x <= xmax and x >= 0 and y <= ymax and y >= 0:
        return True
    else:
        return False


def get_lines(im, rhotheta):

    (ymax, xmax) = np.shape(im)
    lines = []

    for i in range(0, len(rhotheta)):
        point = rhotheta[i]
        rho = point[0]
        theta = point[1] * np.pi / 180 

        # y = mx + b

        m = -np.cos(theta) / np.sin(theta)
        b = rho / np.sin(theta)

        left = (0, b)   # x = 0
        right = (xmax, xmax * m + b) # x = xmax
        top = (-b / m, 0) # y = 0
        bottom = ((ymax - b) / m, ymax) # y = ymax 

        coordinates = [point for point in [left, right, top, bottom]
                       if check_point(point, ymax, xmax)]
        if len(coordinates) == 2:
            (x1, y1) = [int(round(n)) for n in coordinates[0]]
            (x2, y2) = [int(round(n)) for n in coordinates[1]]
            cv2.line(im, (x1, y1), (x2, y2), (0, 0, 255), 1)
            lines.append([x1, y1, x2, y2])

        return lines


pathname = r"C:\Users\Topit\Documents\notebook\set2_1\true_13.jpg"
im = cv2.imread(pathname)
im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
im = cv2.GaussianBlur(im, (5, 5), 0)
edges = cv2.Canny(im, 50, 100)
(rhos, thetas, accumulator) = hough_transform(edges)

rhotheta = peak_values(accumulator, rhos, thetas, 22)
lines = get_lines(im, rhotheta)

cv2.imwrite('lines_img1.png', im)