import cv2
from os.path import realpath, join, dirname
from goal_detector import GoalDetector

# from classify import ShotClassifier

rgb_1 = cv2.imread(join(dirname(realpath(__file__)), '1.jpg'))
rgb_2 = cv2.imread(join(dirname(realpath(__file__)), '2.jpg'))
GoalDetector(scoreboard_type="premier_league").execute(rgb_1, rgb_2)

# ShotClassifier(model_type=1).get_shot_class([rgb_1, rgb_2])
