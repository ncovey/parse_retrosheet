
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

    class play_event_codes(Enum):
        '''
        AP    appeal play
        BP    pop up bunt
        BG    ground ball bunt
        BGDP  bunt grounded into double play
        BINT  batter interference
        BL    line drive bunt
        BOOT  batting out of turn
        BP    bunt pop up
        BPDP  bunt popped into double play
        BR    runner hit by batted ball
        C     called third strike
        COUB  courtesy batter
        COUF  courtesy fielder
        COUR  courtesy runner
        DP    unspecified double play
        E$    error on $
        F     fly
        FDP   fly ball double play
        FINT  fan interference
        FL    foul
        FO    force out
        G     ground ball
        GDP   ground ball double play
        GTP   ground ball triple play
        IF    infield fly rule
        INT   interference
        IPHR  inside the park home run
        L     line drive
        LDP   lined into double play
        LTP   lined into triple play
        MREV  manager challenge of call on the field
        NDP   no double play credited for this play
        OBS   obstruction (fielder obstructing a runner)
        P     pop fly
        PASS  a runner passed another runner and was called out
        R$    relay throw from the initial fielder to $ with no out made
        RINT  runner interference
        SF    sacrifice fly
        SH    sacrifice hit (bunt)
        TH    throw
        TH%   throw to base %
        TP    unspecified triple play
        UINT  umpire interference
        UREV  umpire review of call on the field
        '''
        home_run = 'HR'
        no_play = 'NP'
        bunt_ground_ball = 'BG'
        bunt_popup = 'BP'
        sacrifice_fly = 'SF'
        force_out = 'FO'
        sacrifice_hit = 'SH'
        ground_ball = 'G'
        line_drive = 'L'
        popup = 'P'
        fly_ball = 'F'
        error = 'E' #$
        strikeout = 'K'
        wild_pitch = 'WP'
        passed_ball = 'PB'
        intentional_walk = 'IW'
        walk = 'W'
        stolen_base = 'SB'
        appeal_play ='AP'
        bunt_ground_ball_double_play = 'BGDP'
        batter_interference = 'BINT'
        bunt_line_drive = 'BL'
        batting_out_of_turn = 'BOOT'
        bunt_popup_double_play = 'BPDP'
        runner_hit_by_batted_ball = 'BR'
        called_3rd_strike = 'C'
        courtesy_batter = 'COUB'
        courtesy_fielder = 'COUF'
        courtesy_runner = 'COUR'
        double_play = 'DP' #unspecified
        fly_ball_double_play = 'FDP'
        fan_interference = 'FINT'
        foul = 'FL'
        ground_ball_double_play = 'GDP'
        ground_ball_triple_play = 'GTP'
        infield_fly_rule = 'IF'
        interference = 'INT' #unspecified
        inside_the_park_home_run = 'IPHR'
        lined_into_double_play = 'LDP'
        lined_into_triple_play = 'LTP'
        manager_review = 'MREV'
        no_double_play = 'NDP'
        obstruction = 'OBS'
        runner_pass_out = 'PASS'
        relay_throw = 'R' #$
        runner_interference = 'RINT'
        throw = 'TH' #%
        triple_play = 'TP' #unspecified
        umpire_interference = 'UINT'
        umpire_reivew = 'UREV'
        defensive_interference = 'DI'


    def parse_play_results(self):
        codes = []
        for code in play_record.play_event_codes:
            codes.append(code)
        codes.sort(key = lambda s: len(s.value), reverse=True)
        bFound = False
        for code in codes:
            #print('----{}'.format(code._name_))
            if code.value in self.play_results:
                print (self.play_results, code._name_)
                bFound = True
                break
        if not bFound:
            print ("Could not find a matching code for play: '{}'".format(self.play_results))
        
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

