import cv2
from goal_detector import GoalDetector
from classify import ShotClassifier

frame1 = cv2.cvtColor(cv2.imread('1.jpg'), cv2.COLOR_BGR2GRAY)
frame2 = cv2.cvtColor(cv2.imread('2.jpg'), cv2.COLOR_BGR2GRAY)
GoalDetector().execute([frame1, frame2])


ShotClassifier(model_type=1).get_shot_class([frame1, frame2])