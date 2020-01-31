from Controllers.ImageController import ImageController
from Controllers.ScoreboardTypes import ScoreboardTypes
from GoalDetector.GoalDetector import GoalDetector

_, gray_images = ImageController.read_video_to_memory("third_goal.mp4")
GoalDetector(ScoreboardTypes.PREMIER_LEAGUE).execute(gray_images)
