import numpy as np
import cv2

from GoalDetector.ScoreboardStrategy.Strategy import Strategy
from Controllers.Message import Message


class GoalDetector:
    def __init__(self, scoreboard_type):
        self.__current_scoreboard = scoreboard_type
        self.__strategy = Strategy(scoreboard_type)
        self.__home = '2'
        self.__away = '0'
        self.__home_repeated = ''
        self.__away_repeated = ''
        self.__current_frame = 0

    def extract_scoreboard_results(self, image):
        [home, away] = self.__strategy.extract_results(image)
        if home != "" and away != "":
            if home.isnumeric() and away.isnumeric():
                if home == self.__home and away == self.__away:
                    self.__away_repeated = ''
                    self.__home_repeated = ''
                    return
                if self.__home_repeated == home and self.__away_repeated == away:
                    self.__home = home
                    self.__away = away
                    return True
                self.__home_repeated = home
                self.__away_repeated = away

    def execute(self, gray_images):
        Message.info("Beginning goal detection algorithm")
        frames = []
        goals = []
        cnt = 0
        for gray in gray_images:
            Message.progress(cnt, len(gray_images))
            resized_gray = cv2.resize(
                gray, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

            _, threshold = cv2.threshold(
                resized_gray, 127, 255, cv2.THRESH_BINARY)

            frames.append(threshold)
            if len(frames) == 30:
                images = np.array([np.array(im) for im in frames])
                avg_image = np.sum(images, axis=0)
                avg_image[avg_image >= 255] = 255
                avg_image = avg_image.astype(np.uint8)
                self.__current_frame = cnt
                is_goal = self.extract_scoreboard_results(avg_image)
                if is_goal:
                    goals.append(gray_images[cnt-35*30:cnt+35*30])
                frames.clear()

            cnt += 1
        height, width = gray_images[0].shape
        print(len(goals))
        for idx, goal_frames in enumerate(goals):
            out = cv2.VideoWriter(
                f"goal_{idx + 1}.avi", cv2.VideoWriter_fourcc(*'DIVX'), 15, (width, height))
            for frame in goal_frames:
                out.write(frame)
                out.release()
        Message.success("Goal detection algorithm finished")
