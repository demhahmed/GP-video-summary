import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from os.path import dirname, realpath, join


class GoalDetector:
    def __init__(self, scoreboard_type):
        # loading model
        self.__model = load_model(join(dirname(realpath(__file__)), 'models/ocr.model'))
        # Initialize scoreboard Dimensions.
        if scoreboard_type == 'premier_league':
            # dimensions [height_from, height_to, width_from, width_to]
            self.__height = [64, 80]
            self.__width = [167, 215]
        else:
            raise Exception("Choose a supported scoreboard")

    def __segment_results(self, image):
        v_hist = np.sum(image, axis=0)
        i = 0
        numbers = []
        while i < len(v_hist):
            if v_hist[i] != 0:
                x, y = i, i
                gap = 0
                while y < len(v_hist):
                    y += 1
                    if v_hist[y]:
                        gap = 0
                    if y < len(v_hist) and v_hist[y] == 0:
                        if gap:
                            break
                        else:
                            gap += 1
                numbers.append(image[0:len(image[0]), x:y])
                i = y
            else:
                i += 1
        return numbers

    def __model_result(self, image):
        image = cv2.resize(image, (28, 28))
        image = image.reshape(1, 28, 28, 1)
        return np.argmax(self.__model.predict(image))

    def execute(self, frame_1, frame_2):
        frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
        frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)

        # slicing
        scoreboard_1 = frame_1[self.__height[0]:self.__height[1], self.__width[0]:self.__width[1]]
        scoreboard_2 = frame_2[self.__height[0]:self.__height[1], self.__width[0]:self.__width[1]]

        # thresholding
        _, scoreboard_1 = cv2.threshold(scoreboard_1, 127, 255, cv2.THRESH_BINARY_INV)
        _, scoreboard_2 = cv2.threshold(scoreboard_2, 127, 255, cv2.THRESH_BINARY_INV)

        # resizing
        scoreboard_1 = cv2.resize(scoreboard_1, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
        scoreboard_2 = cv2.resize(scoreboard_2, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

        # erosion
        kernel = np.ones((5, 5), np.uint8)
        scoreboard_1 = cv2.erode(scoreboard_1, kernel, iterations=1)
        # scoreboard_1 = cv2.dilate(scoreboard_1, kernel, iterations=1)
        scoreboard_2 = cv2.erode(scoreboard_2, kernel, iterations=1)
        # scoreboard_2 = cv2.dilate(scoreboard_2, kernel, iterations=1)

        cv2.imwrite("scoreboard_1.jpg", scoreboard_1)
        cv2.imwrite("scoreboard_2.jpg", scoreboard_2)

        numbers = self.__segment_results(scoreboard_1)

        for idx, number in enumerate(numbers):
            cv2.imwrite(f"a{idx}.jpg", number)

        home = self.__model_result(numbers[0])
        away = self.__model_result(numbers[2])

        print(f"home: {home}, away:{away}")
