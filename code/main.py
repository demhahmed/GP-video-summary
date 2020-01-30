from Controllers.ImageController import ImageController
from Controllers.ScoreboardTypes import ScoreboardTypes

ImageController.select_scoreboard(ScoreboardTypes.PREMIER_LEAGUE)

ImageController.read_video_to_memory("first_goal.mp4")
