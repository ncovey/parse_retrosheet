
from enum import Enum
import retrosheet_codes


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
        self.runs_scored = -1 # uninitialized
        self.outs_made = -1
        self.errors = []
        self.base_runner_adv = []
        self.base_hit = False
        #self.parse_play_results()



    def parse_play_results(self):
        num_plays = 0
        print('Inning: {} of the {} | {} |'.format('bottom' if self.is_home else 'top', self.inning, self.player_id))
        print(self.play_results)
        play = self.play_results            
        play_type = retrosheet_codes.get_event_code(play, retrosheet_codes.play_event_codes)
        if play_type != None: print(play_type._name_)
        if (play_type == retrosheet_codes.play_event_codes.no_play):
            print('No play was made')
            self.runs_scored = 0
            self.outs_made = 0
            return
        desc = [] #descriptors
        if ('/' in play):
            _tokens = play.split('/')
            if (len(_tokens) > 1):
                play = _tokens[0]
                desc = _tokens[1:]
        print(play, desc)
        
        # error event:
        error_event = retrosheet_codes.get_event_code(play, retrosheet_codes.fielding_error_event_codes)
        print(error_event._name_ if error_event != None else '')

        hit = retrosheet_codes.get_event_code(play, retrosheet_codes.base_hit_event_codes)
        loc = retrosheet_codes.get_event_code(play, retrosheet_codes.location_codes)
        batted_type = None
        if (hit != None or loc != None):
            batted_type = retrosheet_codes.get_event_code(play, retrosheet_codes.batted_ball_type)
            print ('{} hits a {} into {} for a {}'.format(self.player_id, 
                                                          batted_type._name_ if batted_type != None else '', 
                                                          loc._name_ if loc != None else '', 
                                                          hit._name_ if hit != None else ''))
            self.base_hit = True
            
        if (play_type == retrosheet_codes.play_event_codes.walk or 
        play_type == retrosheet_codes.play_event_codes.intentional_walk or
        play_type == retrosheet_codes.play_event_codes.hit_by_pitch ):
            print('{} reaches base on a {}'.format(self.player_id, play_type._name_))
            self.outs_made = 0
        elif (loc != None):
            out_type = retrosheet_codes.get_event_code(play, retrosheet_codes.out_play_event_codes)
            if play.isdigit() or play.replace('(','').replace(')','').isdigit():
                for m in desc:
                    out_type = retrosheet_codes.get_event_code(m, retrosheet_codes.out_play_event_codes)
                    if out_type != None: 
                        break        
            if hit == None and out_type == None: #this might happen for a simple ground out where only the batted ball type is recorded
                self.outs_made = 1
                for m in desc:
                    batted_type = retrosheet_codes.get_event_code(m, retrosheet_codes.batted_ball_type)
                    if batted_type != None: 
                        break
                print('{} - {}: play made by {}'.format(self.player_id, batted_type._name_ if batted_type != None else '', play))
            elif out_type != None:
                if ((out_type.value != 'NTP') and ('triple_play' in out_type._name_.lower())):
                    self.outs_made = 3
                elif ((out_type.value != 'NDP') and ('double_play' in out_type._name_.lower())):
                    self.outs_made = 2
                else:
                    self.outs_made = 1
                print('{} - {}: play {}'.format(self.player_id, out_type._name_, play))            
            else:
                self.outs_made = 0
        print('{} outs were made on this play'.format(self.outs_made))

        if '.' in desc:
            br = desc.split('.')
            for tok in br:
                advances = tok.split(';')
                for adv in advances:
                    if ('-' in adv):
                        runner, base = adv.split('-')
                        if runner == 'B': runner = "batter's box"
                        if runner == '1': runner = 'first'
                        elif runner == '2': runner = 'second'
                        elif runner == '3': runner = 'third'                                
                        if base == '1': base = 'first'
                        elif base == '2': base = 'second'
                        elif base == '3': base = 'third'
                        elif base == 'H': base = 'home'
                        print ('Runner at {} advances to {} base'.format(runner, base))

        #for code in retrosheet_codes.all_plays_sorted:
        #    if code.value in self.play_results:
        #        num_plays += 1

        #        if code in retrosheet_codes.out_play_event_codes:
        #        else:
        #            # unknown type. possibly an error
        #            self.outs_made = 0

        #        if '/' in self.play_results:
        #            tokens = self.play_results.split('/')
        #            print(tokens)


            
        #        break

        #if num_plays == 0: #not bFound:
        #    print ("Could not find a matching code for play: '{}'".format(self.play_results))
        #elif num_plays > 1:
        #    print ('----------------multiple matches for play')
        
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

