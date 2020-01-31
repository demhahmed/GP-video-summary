import cv2
import numpy as np

from Controllers.Message import Message
from ScoreboardStrategy.Strategy import Strategy


class ImageController:

    __CURRENT_SCOREBOARD = None  # Should be initialized.
    __strategy = None

    @staticmethod
    def select_scoreboard(scoreboard_type):
        ImageController.__CURRENT_SCOREBOARD = scoreboard_type
        ImageController.__strategy = Strategy(scoreboard_type)

    @staticmethod
    def read_image(image_path):
        """ return rgb and gray image """
        bgr_img = cv2.imread(image_path)  # cv2 is dealing with bgr, !important
        return [bgr_img, cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)]

    @staticmethod
    def extract_scoreboard_results(image):
        [home, away] = ImageController.__strategy.extract_results(image)
        Message.info(f"Home: {home}, Away: {away}")

    @staticmethod
    def read_video_to_memory(video_path):
        # Capture video from file
        cap = cv2.VideoCapture(video_path)
        frames = []
        while True:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                cv2.imshow("gray", gray)
                cv2.imshow("rgb", frame)

                resized_gray = cv2.resize(gray, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
                _, threshold = cv2.threshold(resized_gray, 127, 255, cv2.THRESH_BINARY)
                frames.append(threshold)
                if len(frames) == 30:
                    images = np.array([np.array(im) for im in frames])
                    avg_image = np.sum(images, axis=0)
                    avg_image[avg_image >= 255] = 255
                    avg_image = avg_image.astype(np.uint8)
                    cv2.imwrite("0.png", avg_image)
                    ImageController.extract_scoreboard_results(avg_image)
                    frames.clear()
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
