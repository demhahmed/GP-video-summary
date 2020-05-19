
class shot:
    __slots__ = ("frame_number", "shot_start", "shot_end",
                 "type", "has_goal", "has_goal_mouth", "audio")

    def __init__(self, frame_number, shot_start, shot_end, type=None, has_goal=None, has_goal_mouth=None, audio=None):
        self.frame_number = frame_number
        self.shot_start = shot_start
        self.shot_end = shot_end
        self.type = type if type is not None else False
        self.has_goal = has_goal if has_goal is not None else False
        self.has_goal_mouth = has_goal_mouth if has_goal_mouth is not None else False
        self.audio = audio if audio is not None else False

    def __repr__(self):
        return str(self)

    def __str__(self):
        shot_info = "frame_number: {0} | start: {1} | end: {2} | type: {3} | goal: {4} | goal_mouth: {5} | audio: {6} {7}".format(
            self.frame_number, self.shot_start, self.shot_end, self.type, self.has_goal, self.has_goal_mouth, self.audio, "\n")
        return shot_info


class shot_types:
    __slots__ = ('LOGO', 'WIDE', 'MEDIUM', 'CLOSE', 'CLOSE_OUT')

    def __init__(self):
        self.LOGO = 'logo'
        self.WIDE = 'wide'
        self.MEDIUM = 'medium'
        self.CLOSE = 'close'
        self.CLOSE_OUT = 'close-out'


class event_types:
    __slots__ = ('GOAL', 'ATTACK', 'OTHER')

    def __init__(self):
        self.GOAL = 'goal'
        self.ATTACK = 'attack'
        self.OTHER = 'other'
