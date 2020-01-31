from Controllers.App import App
from Controllers.ScoreboardTypes import ScoreboardTypes

# rbg_images, gray_images, fps = ImageController.read_video_to_memory("match.mp4")
# GoalDetector(ScoreboardTypes.PREMIER_LEAGUE).execute(gray_images, fps)

if __name__ == "__main__":
    app = App("match.mp4", ScoreboardTypes.PREMIER_LEAGUE)
    app.start()