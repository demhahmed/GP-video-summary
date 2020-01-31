import cv2
import os.path
from threading import Thread

from Controllers.ImageController import ImageController
from Controllers.Message import Message
from Controllers.ScoreboardTypes import ScoreboardTypes
from GoalDetector.GoalDetector import GoalDetector


class App:
    def __init__(self, video_name, scoreboard_type):
        self.__video_name = video_name
        self.__scoreboard_type = scoreboard_type
        self.__fps = 0
        self.__frame_cnt = 0
        self.__capacity = 1000
        if not os.path.isfile(video_name):
            Message.error("File does not exist, please select a valid video w.r.t the 'code/' path")
            exit(0)
        if self.__scoreboard_type not in ScoreboardTypes:
            Message.error("Sorry, this scoreboard is not supported right not")
            exit(0)
        self.__goal_detector = GoalDetector(scoreboard_type)
        Message.info("Scoreboard has been loaded successfully")

    def goal_detection(self, gray_frames, cnt):
        is_goal = self.__goal_detector.execute(gray_frames)
        if is_goal:
            start_time = float(max(cnt - 30 * self.__fps, 0)) / self.__fps
            end_time = float(min(cnt + 50 * self.__fps, self.__frame_cnt - 1)) / self.__fps
            self.save_goal_detection_output(start_time, end_time)

    def logo_detection(self, rgb_frames, gray_frames, cnt):
        pass

    def distribute_work(self, rgb_frames, gray_frames, cnt, goal_detection_frames):
        gd_thread = None
        if len(goal_detection_frames) == int(self.__fps * 5):
            gd_thread = Thread(target=self.goal_detection, args=(goal_detection_frames, cnt))
            gd_thread.start()
        ld_thread = Thread(target=self.logo_detection, args=(rgb_frames, gray_frames, cnt))
        ld_thread.start()
        if gd_thread:
            gd_thread.join()
            goal_detection_frames.clear()
        ld_thread.join()

    def save_goal_detection_output(self, start_time, end_time):
        with open("goals.txt", mode='a') as file:
            file.write(f"Goal: {str(start_time)}\t{str(end_time)}\n")

    def start(self):
        Message.info("Reading Video: in-progress")
        cap = cv2.VideoCapture(self.__video_name)  # Capture video from file
        self.__fps = cap.get(cv2.CAP_PROP_FPS)
        self.__frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        total_bgr_frames = []
        total_gray_frames = []
        goal_detection_frames = []
        cnt = 0  # to keep track how many frames has been read
        idx = 0  # just for dynamic list ( shrink, expand )
        while cap.isOpened() or cnt == self.__frame_cnt:
            Message.progress(cnt, self.__frame_cnt, 50)
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                if len(total_gray_frames) >= self.__capacity:
                    total_gray_frames = total_gray_frames[100:]
                    total_bgr_frames = total_bgr_frames[100:]
                    idx -= 100
                total_gray_frames.append(gray)
                total_bgr_frames.append(frame)
                goal_detection_frames.append(gray)
                self.distribute_work(total_bgr_frames, total_gray_frames, cnt, goal_detection_frames)
                cv2.imshow("rgb", frame)
                cv2.imshow("gray", gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cnt += 1
            idx += 1
        cap.release()
        Message.info("Reading Video: done")
