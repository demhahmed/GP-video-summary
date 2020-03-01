import cv2
from os.path import dirname, realpath, join
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model

class GoalDetector:
    def __init__(self, scoreboard_type='premier_league'):
        # loading model
        self.__model = load_model(
            join(dirname(realpath(__file__)), 'ocr.model'))
        if scoreboard_type == 'premier_league':
            # dimensions [height_from, height_to, width_from, width_to]
            self.__home_dim = [60, 80, 165, 187]
            self.__away_dim = [60, 80, 192, 215]

    def execute(self, frame_1, frame_2):
        # convert rgb to gray
        frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
        frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)
        
        # mask the home, away
        home_image = frame_1[self.__home_dim[0]:self.__home_dim[1],
                             self.__home_dim[2]:self.__home_dim[3]]
        away_image = frame_2[self.__away_dim[0]:self.__away_dim[1],
                             self.__away_dim[2]:self.__away_dim[3]]

        # threshold
        _, home_image = cv2.threshold(home_image, 127, 255, cv2.THRESH_BINARY)
        _, away_image = cv2.threshold(away_image, 127, 255, cv2.THRESH_BINARY)

        # resized
        home_image = cv2.resize(home_image, (28, 28))
        away_image = cv2.resize(away_image, (28, 28))

        cv2.imwrite('home.jpg', home_image)
        cv2.imwrite('away.jpg', away_image)

        # reshaped
        home_image = home_image.reshape(1, 28, 28, 1)
        away_image = away_image.reshape(1, 28, 28, 1)

        # model predict
        home = self.__model.predict(home_image)
        away = self.__model.predict(away_image)

        print(home.argmax())
        print(away.argmax())
        

class PyTesseract(GoalDetector):
    def __init__(self, scoreboard_type='premier_league'):
        


rgb_1 = cv2.imread('1.jpg')
rgb_2 = cv2.imread('2.jpg')
GoalDetector().execute(rgb_1, rgb_2)
