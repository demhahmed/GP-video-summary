import cv2
import numpy as np
from skimage.measure import compare_ssim


class GoalDetector:
    def __init__(self, scoreboard_type):
        # loading model
        # Initialize scoreboard Dimensions.
        if scoreboard_type == 'premier_league':
            # dimensions [height_from, height_to, width_from, width_to]
            self.__height = [64, 80]
            self.__width = [167, 215]
            self.__home = None
            self.__away = None
            self.__sepr = None
        else:
            raise Exception("Choose a supported scoreboard")

    def __segment_results(self, image):
        if self.__home is not None:
            home = image[self.__home[0]:self.__home[1], self.__home[2]:self.__home[3]]
            sepr = image[self.__sepr[0]:self.__sepr[1], self.__sepr[2]:self.__sepr[3]]
            away = image[self.__away[0]:self.__away[1], self.__away[2]:self.__away[3]]
            return home, sepr, away
        v_hist = np.sum(image, axis=0)
        print(v_hist)
        i = 0
        numbers, dimensions = [], []
        while i < len(v_hist):
            if v_hist[i] != 0:
                x, y = i, i
                gap = 0
                while y < len(v_hist):
                    y += 1
                    if v_hist[y]:
                        gap = 0
                    if y < len(v_hist) and v_hist[y] == 0:
                        if gap == 2:
                            break
                        else:
                            gap += 1
                if y - x >= 10:
                    dimensions.append([0, len(image), x, y])
                    numbers.append(image[0:len(image), x:y])
                i = y
            else:
                i += 1
        if len(numbers) == 3:
            self.__home, self.__sepr, self.__away = dimensions[0], dimensions[1], dimensions[2]
        return numbers

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
        kernel = np.ones((3, 3), np.uint8)
        scoreboard_1 = cv2.erode(scoreboard_1, kernel, iterations=1)
        # scoreboard_1 = cv2.dilate(scoreboard_1, kernel, iterations=1)
        scoreboard_2 = cv2.erode(scoreboard_2, kernel, iterations=1)
        # scoreboard_2 = cv2.dilate(scoreboard_2, kernel, iterations=1)

        first_results = self.__segment_results(scoreboard_1)
        later_results = self.__segment_results(scoreboard_2)

        for idx, number in enumerate(first_results):
            cv2.imwrite(f"first{idx}.jpg", number)

        for idx, number in enumerate(later_results):
            cv2.imwrite(f"second{idx}.jpg", number)

        if len(first_results) == len(later_results) and len(first_results) == 3:
            home_score, _ = compare_ssim(first_results[0], later_results[0], full=True)
            away_score, _ = compare_ssim(first_results[2], later_results[2], full=True)
            print(home_score, away_score)
            if home_score * 100 <= 80:
                print("Home Score Changed")
                return True
            elif away_score * 100 <= 80:
                print("Away Score Changed")
                return True
            else:
                print("No Change")
                return False
