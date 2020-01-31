from pytesseract import image_to_string
import cv2
import numpy as np

class Scoreboard:
    def extract_results(self, image):
        pass


class PLScoreboard(Scoreboard):
    def extract_results(self, image):
        # _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
        config = "--psm 7" #--oem 3 -c tessedit_char_whitelist=0123456789

        scale = 5
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

        # HOME TEAM
        temp = image[60*scale:80*scale, 165*scale:185*scale]
        home_team_image = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        cv2.imshow("home", home_team_image)
        home_team = image_to_string(home_team_image, lang="eng", config=config)

        # AWAY TEAM
        temp = image[60*scale:80*scale, 192*scale:215*scale]
        away_team_image = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        cv2.imshow("away", away_team_image)
        away_team = image_to_string(away_team_image, lang="eng", config=config)

        return home_team, away_team


class LaLigaScoreboard(Scoreboard):
    def extract_results(self, image):
        # to be implemented.
        pass


class SeriaAScoreboar(Scoreboard):
    def extract_results(self, image):
        # to be implemented.
        pass


class UCL2019(Scoreboard):
    def extract_results(self, image):
        # to be implemented.
        pass


class UCL2018(Scoreboard):
    def extract_results(self, image):
        # to be implemented.
        pass
