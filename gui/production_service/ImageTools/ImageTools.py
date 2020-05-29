import numpy as np
import cv2


class ImageTools:

    BINARY = 'BINARY'
    INV_BINARY = 'INV_BINARY'

    @staticmethod
    def threshold(image, center, threshold_type):
        """ image  -> bgr image
            center -> the value which is treaded as threshold
            threshold_type -> INV_BINARY or BINARY
        """
        low = 0 if threshold_type == ImageTools.BINARY else 255
        high = 255 if low == 0 else 0
        return np.array(np.where(image <= center, low, high))

    @staticmethod
    def image_to_gray(image):
        """ Takes Image with channels b, g, r respectively """
        # Y = 0.2125 R + 0.7154 G + 0.0721 B
        gray_image = image.copy()
        return np.array(0.2125 * gray_image[:, :, 2] + 0.7154 * gray_image[:, :, 1] + 0.0721 * gray_image[:, :, 0])

    @staticmethod
    def surrounding_pixels(image, kernel_size, i, j):
        values = []
        dir = (kernel_size // 2) // 2  # directions
        for idx_i in range(-dir, dir + 1):
            for idx_j in range(-dir, dir + 1):
                values.append(image[i + idx_i, j + idx_j])
        return values

    @staticmethod
    def erode(image, kernel_size):
        """ Apply Min Filter """
        if kernel_size % 2 != 1:
            raise Exception('Erode Kernel Must be odd')
        space = kernel_size // 2
        copy = image.copy()
        for i in range(space, len(image) - space):
            for j in range(space, len(image[0]) - space):
                surroundings = ImageTools.surrounding_pixels(
                    image, kernel_size, i, j)
                copy[i, j] = np.min(surroundings)
        return np.array(copy)

    @staticmethod
    def dilate(image, kernel_size):
        """ Apply Max Filter """
        if kernel_size % 2 != 1:
            raise Exception('Dilate Kernel Must be odd')
        space = kernel_size // 2
        copy = image.copy()
        for i in range(space, len(image) - space):
            for j in range(space, len(image[0]) - space):
                surroundings = ImageTools.surrounding_pixels(
                    image, kernel_size, i, j)
                copy[i, j] = np.max(surroundings)
        return np.array(copy)

    @staticmethod
    def image_similarity_ratio(image_1, image_2):
        image_1 = ImageTools.threshold(image_1, 127, ImageTools.BINARY)
        image_2 = ImageTools.threshold(image_2, 127, ImageTools.BINARY)
        height_1, width_1 = image_1.shape
        height_2, width_2 = image_2.shape
        if height_1 != height_2 or width_1 != width_2:
            raise Exception("Two Images Must have same dimensions")
        similar = 0
        for i in range(len(image_1)):
            for j in range(len(image_1)):
                if image_1[i, j] == image_2[i, j]:
                    similar += 1
        return (similar / (height_1 * width_1)) * 100

    @staticmethod
    def histogram(image):
        histogram = [0] * 256
        for i in range(len(image)):
            for j in range(len(image)):
                histogram[image[i, j]] += 1
        return histogram

    @staticmethod
    def image_dominant_color(image):
        frame = np.array(image)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))
        # slice the green
        imask = mask > 0
        frame[imask] = 255
        frame[~imask] = 0
        # frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR) # RGB color to HLS
        # RGB color to gray level
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, frame = cv2.threshold(frame, 127, 255, 0)
        return frame

    @staticmethod
    def image_dominant_color_ratio(image):
        frame = ImageTools.image_dominant_color(image)
        percentage = np.sum(frame == 255) / (frame.shape[0] * frame.shape[1])
        return percentage