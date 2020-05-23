from Controllers.ScoreboardTypes import ScoreboardTypes
from GoalDetector.ScoreboardStrategy.Scoreboard import PLScoreboard, LaLigaScoreboard, SeriaAScoreboar, UCL2019, UCL2018


class Strategy:

    def __init__(self, scoreboard_type):
        if scoreboard_type == ScoreboardTypes.PREMIER_LEAGUE:
            self.strategy = PLScoreboard()
        elif scoreboard_type == ScoreboardTypes.LA_LIGA:
            self.strategy = LaLigaScoreboard()
        elif scoreboard_type == ScoreboardTypes.SERIA_A:
            self.strategy = SeriaAScoreboar()
        elif scoreboard_type == ScoreboardTypes.CHAMPIONS_LEAGUE_2019:
            self.strategy = UCL2019()
        elif scoreboard_type == ScoreboardTypes.CHAMPIONS_LEAGUE_2018:
            self.strategy = UCL2018()

    def extract_results(self, image):
        return self.strategy.extract_results(image)
