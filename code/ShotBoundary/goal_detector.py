import cv2
import pytesseract

# Setup Environment for tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class GoalDetector:
    def __init__(self):
        self.__home = '0'
        self.__away = '0'
        self.__home_repeated = ''
        self.__away_repeated = ''

    def __premier_league_scoreboard(self, image):
        """ extracts the results from premier league scoreboard """
        config = '--psm 7'
        scale = 2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        temp = image[60 * scale:80 * scale, 165 * scale:185 * scale]
        home_team_image = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        cv2.imwrite("home.jpg", home_team_image)
        home_team = pytesseract.image_to_string(
            home_team_image, lang='eng', config=config)
        temp = image[60 * scale:80 * scale, 192 * scale:215 * scale]
        away_team_image = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        cv2.imwrite("away.jpg", away_team_image)
        away_team = pytesseract.image_to_string(
            away_team_image, lang='eng', config=config)
        return home_team, away_team

    def __extract_scoreboard_results(self, image):
        [home, away] = self.__premier_league_scoreboard(image)
        print(f'home:{home} away:{away}')
        if home != '' and away != '':
            if home.isnumeric() and away.isnumeric():
                if home == self.__home and away == self.__away:
                    self.__away_repeated = ''
                    self.__home_repeated = ''
                    return
                if self.__home_repeated == home and self.__away_repeated == away:
                    self.__home = home
                    self.__away = away
                    return True
                self.__home_repeated = home
                self.__away_repeated = away

    def execute(self, frames):
        scale = 2

        begin_frame = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        end_frame = cv2.cvtColor(frames[1], cv2.COLOR_BGR2GRAY)

        begin_frame = cv2.resize(
            begin_frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        end_frame = cv2.resize(end_frame, None, fx=scale,
                               fy=scale, interpolation=cv2.INTER_CUBIC)

        _, begin_frame = cv2.threshold(
            begin_frame, 127, 255, cv2.THRESH_BINARY)
        _, end_frame = cv2.threshold(begin_frame, 127, 255, cv2.THRESH_BINARY)

        is_goal = self.__extract_scoreboard_results(begin_frame)
        is_goal = self.__extract_scoreboard_results(end_frame)
        if is_goal:
            print('Goal Detected')
        return is_goal
