
from enum import Enum

class pitchres(Enum):
    # pitch result
    called_strike = 'C'
    swinging_strike = 'S'
    ball = 'B'
    foul = 'F'
    pickoff_first = '1'
    pickoff_second = '2'
    pickoff_third = '3'
    foul_bunt = 'L'
    missed_bunt = 'M'
    swinging_strike_pitchout = 'Q'
    foul_pitchout = 'R'
    intentional_ball = 'I'
    pitchout = 'P'
    hit_by_pitch = 'H'
    strike = 'K'
    unknown = 'U'
    in_play = 'X'
    in_play_pitchout = 'Y'

class pitchres_mod(Enum):
    # these are modifiers that come after the pitch result
    catcher_pickoff = '+'
    catcher_blocked_pitch = '*'
    runner_going = '>'


class fpos(Enum):
    # fielding position
    invalid = 0
    P = 1
    C = 2
    B1 = 3 #1B
    B2 = 4 #2B
    B3 = 5 #3B
    SS = 6
    LF = 7
    CF = 8
    RF = 9
    DH = 10
    # for subs
    PH = 11
    PR = 12
    @staticmethod
    def ntofpos(n):
        for pos in fpos:
            if n == pos.value:
                return pos
    @staticmethod
    def getname(fp):
        if (fp in fpos):
            if (fp == fpos.P):
                return 'Pitcher'
            elif (fp == fpos.C):
                return 'Catcher'
            elif (fp == fpos.B1):
                return 'First Base'
            elif (fp == fpos.B2):
                return 'Second Base'
            elif (fp == fpos.B3):
                return 'Third Base'
            elif (fp == fpos.SS):
                return 'Shortstop'
            elif (fp == fpos.LF):
                return 'Left Field'
            elif (fp == fpos.CF):
                return 'Center Field'
            elif (fp == fpos.RF):
                return 'Right Field'
            elif (fp == fpos.DH):
                return 'Designated Hitter'
            elif (fp == fpos.PH):
                 return 'Pinch Hitter'
            elif (fp == fpos.PR):
                 return 'Pinch Runner'
        else:
            return None

class record_type(Enum):
    # record type
    invalid = 0
    id = 'id'
    version = 'version'
    info = 'info'
    start = 'start'
    play = 'play'
    com = 'com'
    sub = 'sub'
    data = 'data'

class record:
    def __init__(self, tokens=[]):
        self._type = record_type.invalid
        self._values = None
        if (len(tokens) is not 0):
            if hasattr(record_type, tokens[0]):
                self._type = tokens[0]
                self._values = tokens[1:]

class starter_record(record):
    def __init__(self, tokens = []):
        record.__init__(self, tokens)
        self.player_id = self._values[0]
        self.name = self._values[1]
        self.is_home = True if int(self._values[2]) is 1 else False
        self.batting_order = self._values[3]
        self.start_field_pos = fpos.ntofpos(int(self._values[4]))

class play_record(record):
    def __init__(self, tokens = []):
        record.__init__(self, tokens)
        self.inning = self._values[0]
        self.is_home = True if int(self._values[1]) is 1 else False
        self.player_id = self._values[2]
        self.count = list(self._values[3])
        self.pitch_results = list(self._values[4])
        self.play_results = self._values[5] #(self._values[5].split(',')) # should not contain commas! this might be a bug in the EVN sheet
    def parse_play_results(self):
        for 
        
class sub_record(record):
    def __init__(self, tokens = []):
        record.__init__(self, tokens)
        self.player_id = self._values[0]
        self.name = self._values[1]
        self.is_home = True if int(self._values[2]) is 1 else False
        self.batting_order = self._values[3]
        self.sub_field_pos = fpos.ntofpos(int(self._values[4]))

class game_record:
    def __init__(self):
        self.id = ''
        self.ver = ''
        self.info = []
        self.starters = []
        self.plays = []
        self.comments = []
        self.substitutions = []
        self.data = []
    def add(self, tokens=[]):
        tk = tokens[0]
        if (tk == record_type.version.value):
            self.ver = tokens[1]
        elif (tk == record_type.info.value):
            self.info.append(record(tokens))
        elif (tk == record_type.start.value):
            self.starters.append(starter_record(tokens))
        elif (tk == record_type.play.value):
            self.plays.append(play_record(tokens))
        elif (tk == record_type.com.value):
            self.comments.append(record(tokens))
        elif (tk == record_type.sub.value):
            #self.substitutions.append(record(tokens))
            self.plays.append(sub_record(tokens))
        elif (tk == record_type.data.value):
            self.data.append(record(tokens))

