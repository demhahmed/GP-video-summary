import cv2

from Controllers.Message import Message

class ImageController:

    @staticmethod
    def read_image(image_path):
        """ return rgb and gray image """
        bgr_img = cv2.imread(image_path)  # cv2 is dealing with bgr, !important
        return [bgr_img, cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)]

    @staticmethod
    def read_video_to_memory(video_path):
        Message.info("Reading Video: in-progress")
        cap = cv2.VideoCapture(video_path)  # Capture video from file
        total_bgr_frames = []
        total_gray_frames = []
        while True:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                total_gray_frames.append(gray)
                total_bgr_frames.append(frame)
            else:
                Message.success("Reading Video: done")
                break
        cap.release()
        return total_bgr_frames, total_gray_frames
