from pytesseract import image_to_string
import cv2


class PLScoreboard:
    """ premier league scoreboard controller """

    def extract_results(self, image):
        """ extracts the results from premier league scoreboard """

        # _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
        # config = "--psm 7"  # --oem 3 -c tessedit_char_whitelist=0123456789
        config = "--psm 7"
        scale = 2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        cv2.imwrite("img.png", image)
        # HOME TEAM
        temp = image[60 * scale:80 * scale, 165 * scale:185 * scale]
        home_team_image = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        home_team = image_to_string(home_team_image, lang="eng", config=config)
        cv2.imwrite("home.png", temp)
        # AWAY TEAM
        temp = image[60 * scale:80 * scale, 192 * scale:215 * scale]
        away_team_image = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        away_team = image_to_string(away_team_image, lang="eng", config=config)
        cv2.imwrite("away.png", temp)
        return home_team, away_team


class LaLigaScoreboard:
    """ LA_LIGA scoreboard controller """

    def extract_results(self, image):
        """ extracts the results from LA_LIGA scoreboard """
        # to be implemented.
        pass


class SeriaAScoreboar:
    """ SERIA_A scoreboard controller """

    def extract_results(self, image):
        """ extracts the results from SERIA_A scoreboard """
        # to be implemented.
        pass


class UCL2019:
    """ CHAMPIONS_LEAGUE_2019 scoreboard controller """

    def extract_results(self, image):
        """ extracts the results from CHAMPIONS_LEAGUE_2019 scoreboard """
        # to be implemented.
        pass


class UCL2018:
    """ CHAMPIONS_LEAGUE_2018 scoreboard controller """

    def extract_results(self, image):
        """ extracts the results from CHAMPIONS_LEAGUE_2018 scoreboard """
        # to be implemented.
        pass
