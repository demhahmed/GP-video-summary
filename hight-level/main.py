import cv2
from goal_detector import GoalDetector
# from classify import ShotClassifier
from os.path import dirname, realpath, join
import sys


def progress(value, end_value, bar_length=20) -> None:
    """ Prints progress bar """
    percent = float(value) / end_value
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f"\rPercent: [{arrow + spaces}] {int(round(percent * 100))}%")
    sys.stdout.flush()

cap = cv2.VideoCapture('1.mp4')  # Capture video from file
frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cnt = 0
goal_detector = GoalDetector()
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    progress(cnt, frame_cnt, 20)
    if cnt % 10 == 0:
        frames.append(frame)
    if len(frames) % 2 == 0 and len(frames) > 0:
        if goal_detector.execute(frames[0], frames[1]):
            cv2.imwrite(f'{cnt}.jpg', frames[0])
            cv2.imwrite(f'{cnt + 1}.jpg', frames[1])
        frames.clear()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cnt += 1
cap.release()

# rgb_1 = cv2.imread(join(dirname(realpath(__file__)), '1.jpg'))
# rgb_2 = cv2.imread(join(dirname(realpath(__file__)), '2.jpg'))
# GoalDetector().execute(rgb_1, rgb_2)

# ShotClassifier(model_type=1).get_shot_class([rgb_1, rgb_2])
