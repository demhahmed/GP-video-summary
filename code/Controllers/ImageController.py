import cv2
import pytesseract as ocr
from Message import Message
from ScoreboardTypes import ScoreboardTypes


class ImageController:

    __CURRENT_SCOREBOARD = None  # Should be initialized.

    @staticmethod
    def select_scoreboard(scoreboard_type):
        ImageController.__CURRENT_SCOREBOARD = scoreboard_type

    @staticmethod
    def convert_image_to_rbg_gray(image):
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return [rgb_img, gray_img]

    @staticmethod
    def read_image(image_path):
        """ return rgb and gray image """
        bgr_img = cv2.imread(image_path)  # cv2 is reading image BGR not RGB
        return ImageController.convert_image_to_rbg_gray(bgr_img)

    @staticmethod
    def extract_scoreboard_results(image):
        pass

    @staticmethod
    def read_video_to_memory(video_path):
        # Capture video from file
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                cv2.imshow("gray", gray)
                cv2.imshow("rgb", frame)
                Message.info(ocr.image_to_string(gray, lang='eng'))
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
