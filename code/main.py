from Controllers.ImageController import ImageController
from Controllers.ScoreboardTypes import ScoreboardTypes
from GoalDetector.GoalDetector import GoalDetector

rbg_images, gray_images, fps = ImageController.read_video_to_memory("third_goal.mp4")
GoalDetector(ScoreboardTypes.PREMIER_LEAGUE).execute(gray_images, fps)

