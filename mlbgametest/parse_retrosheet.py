
from enum import Enum
import retrosheet_codes
from retrosheet_codes import fielding_position_codes as fpos
import re
import sys

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

    @staticmethod
    def parse_modifiers(play):
        #play = 'S8/G.1-2'
        desckeys = '/.;'
        def between_parens(s, chr):
            if chr not in s:
                return False
            paren_idxes = map(None, 
            [i for (i, a) in enumerate(play) if a == '('], 
            [i for (i, a) in enumerate(play) if a == ')'])
            for p in paren_idxes:
                o,c = p
                if s.find(chr) in range(o, c):
                    return True
            return False            
        def parse_token(_play, tkn='/'):
            lp = None
            for _tkn in desckeys:
                if _tkn in _play and not between_parens(_play, _tkn):
                    lp = _play.split(_tkn, 1)
                    break
            if lp == None: return [_play]
            for n, l in enumerate(lp):
                for c in desckeys:
                    if c in l and not between_parens(l, c):
                        lp[n] = parse_token(l, c)
            return lp        
        def parse_parentheses(_lp):
            if len(_lp) > 0:
                for i, p in enumerate(_lp):
                    if type(p) is str and ('(' in p) and (')' in p):
                        parse_paren = p                
                        tmp = []
                        while ('(' in parse_paren) and (')' in parse_paren):                    
                            _open = parse_paren.find('(')
                            _close = parse_paren.find(')')
                            if (_open == -1 or _close == -1) or (_open > _close):
                                print('Warning: could not complete parentheses')
                                break
                            _str_open = parse_paren[:_open]
                            if (_str_open != ''):
                                tmp.append(_str_open)
                            tmp.append(parse_token(parse_paren[_open + 1:_close]))
                            parse_paren = parse_paren[_close + 1:]
                        if (parse_paren != ''):
                            tmp.append(parse_paren)
                        _lp[i] = tmp
                    elif type(p) is list:
                        _lp[i] = parse_parentheses(p)
                    else:
                        continue
            return _lp
        list_play = parse_token(play)
        list_play = parse_parentheses(list_play)
        return list_play

    def parse_play_results(self):
        num_plays = 0
        #print('Inning: {} of the {} | {} |'.format('bottom' if self.is_home else 'top', self.inning, self.player_id))
        #print(self.play_results)

        #parsed_results = play_record.parse_modifiers(self.play_results)
        #print(parsed_results)

        #def parse_group(_group, depth=0):
        #    for i, elmt in enumerate(_group):
        #        if type(elmt) is list:
        #            parse_group(elmt, depth+1)
        #        elif type(elmt) is str:                    
        #            evt = retrosheet_codes.get_event_code(elmt)
        #            if evt != None:
        #                print('{}{}\t{}'.format((''.join('|---' for _ in range(0, depth))), elmt, evt._name_))
        #            else:
        #                print('unknown code: {}'.format(elmt))

                    # seems like the first element is always used to indicate if a hit or an out was made

        #parse_group(parsed_results)
        results = retrosheet_codes.play_formats.matches_format(self.play_results)


        #play = self.play_results
        #for play in parsed_results:
        #    play_type = retrosheet_codes.get_event_code(play, retrosheet_codes.play_event_codes)
        #    if play_type != None: print(play_type._name_)
        #    if (play_type == retrosheet_codes.play_event_codes.no_play):
        #        print('No play was made')
        #        self.runs_scored = 0
        #        self.outs_made = 0
        #        return
        #    desc = [] #descriptors
        #    if ('/' in play):
        #        _tokens = play.split('/')
        #        if (len(_tokens) > 1):
        #            play = _tokens[0]
        #            desc = _tokens[1:]
        #    print(play, desc)
        
        #    # error event:
        #    error_event = retrosheet_codes.get_event_code(play, retrosheet_codes.fielding_error_event_codes)
        #    if error_event != None:
        #        print('error(s) made: {}'.format(error_event._name_))

        #    hit = retrosheet_codes.get_event_code(play, retrosheet_codes.base_hit_event_codes)
        #    loc = retrosheet_codes.get_event_code(play, retrosheet_codes.location_codes)
        #    batted_type = None
        #    if (hit != None or loc != None):
        #        batted_type = retrosheet_codes.get_event_code(play, retrosheet_codes.batted_ball_type)
        #        print ('{} hits a {} into {} for a {}'.format(self.player_id, 
        #                                                      batted_type._name_ if batted_type != None else '', 
        #                                                      loc._name_ if loc != None else '', 
        #                                                      hit._name_ if hit != None else ''))
        #        self.base_hit = True
        #        self.outs_made = 0
            
        #    if (play_type == retrosheet_codes.play_event_codes.walk or 
        #    play_type == retrosheet_codes.play_event_codes.intentional_walk or
        #    play_type == retrosheet_codes.play_event_codes.hit_by_pitch ):
        #        print('{} reaches base on a {}'.format(self.player_id, play_type._name_))
        #        self.outs_made = 0
        #    elif (play_type == retrosheet_codes.out_play_event_codes.strikeout):
        #        print('{} was struck out'.format(self.player_id, play_type._name_))
        #        self.outs_made = 1
        #    elif (loc != None):
        #        out_type = retrosheet_codes.get_event_code(play, retrosheet_codes.out_play_event_codes)
        #        if play.isdigit() or play.replace('(','').replace(')','').isdigit():
        #            for m in desc:
        #                out_type = retrosheet_codes.get_event_code(m, retrosheet_codes.out_play_event_codes)
        #                if out_type != None: 
        #                    break        
        #        if hit == None and out_type == None: #this might happen for a simple ground out where only the batted ball type is recorded
        #            self.outs_made = 1
        #            for m in desc:
        #                batted_type = retrosheet_codes.get_event_code(m, retrosheet_codes.batted_ball_type)
        #                if batted_type != None: 
        #                    break
        #            print('{} - {}: play made by {}'.format(self.player_id, batted_type._name_ if batted_type != None else '', play))
        #        elif out_type != None:
        #            if ((out_type.value != 'NTP') and ('triple_play' in out_type._name_.lower())):
        #                self.outs_made = 3
        #            elif ((out_type.value != 'NDP') and ('double_play' in out_type._name_.lower())):
        #                self.outs_made = 2
        #            else:
        #                self.outs_made = 1
        #            print('{} - {}: play {}'.format(self.player_id, out_type._name_, play))            
        #        else:
        #            self.outs_made = 0
        #    print('{} outs were made on this play'.format(self.outs_made))

        #    if '.' in desc:
        #        br = desc.split('.')
        #        for tok in br:
        #            advances = tok.split(';')
        #            for adv in advances:
        #                if ('-' in adv):
        #                    runner, base = adv.split('-')
        #                    if runner == 'B': runner = "batter's box"
        #                    if runner == '1': runner = 'first'
        #                    elif runner == '2': runner = 'second'
        #                    elif runner == '3': runner = 'third'                                
        #                    if base == '1': base = 'first'
        #                    elif base == '2': base = 'second'
        #                    elif base == '3': base = 'third'
        #                    elif base == 'H': base = 'home'
        #                    print ('Runner at {} advances to {} base'.format(runner, base))

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

