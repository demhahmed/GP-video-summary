import cv2
from skimage.measure import compare_ssim


class GoalDetector:
    def __init__(self, scoreboard_type='premier_league'):
        if scoreboard_type == 'premier_league':
            self.__height = [60, 80]
            self.__width = [165, 215]

    def execute(self, frame_1, frame_2):
        frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
        frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)

        # slicing
        scoreboard_1 = frame_1[self.__height[0]:self.__height[1], self.__width[0]:self.__width[1]]
        scoreboard_2 = frame_2[self.__height[0]:self.__height[1], self.__width[0]:self.__width[1]]

        # check similarity index
        score, _ = compare_ssim(scoreboard_1, scoreboard_2, full=True)
        
        if 40 <= score * 100 <= 90:
            print('Goal Detected')
            return True
