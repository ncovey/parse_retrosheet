
from enum import Enum
import retrosheet_codes
from retrosheet_codes import fielding_position_codes as fpos
import re
import sys
import time

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
        self.play_formats = []
        #self.parse_play_results()


    def parse_play_results(self):
        play_res = ''
        if '!' in self.play_results or '?' in self.play_results:
            play_res = self.play_results.replace('!', '').replace('?', '')
        else:
            play_res = self.play_results
        
        results = retrosheet_codes.play_formats.matches_format(play_res)

        if len(results) > 0:
            for res in results:
                #self.play_formats.append(res[0])
                #print('"{}" - {} ({})'.format(self.play_results, res[0], res[1]))
                if (res[0] == retrosheet_codes.play_formats.single or
                    res[0] == retrosheet_codes.play_formats.double or
                    res[0] == retrosheet_codes.play_formats.triple or
                    res[0] == retrosheet_codes.play_formats.home_run or
                    res[0] == retrosheet_codes.play_formats.inside_the_park_home_run):
                    self.base_hit = True
                    
            if self.base_hit == True and not any(res[0] == retrosheet_codes.play_formats.putout_baserunner for res in results) :
                self.outs_made = -1

            else:
                for res in results:
                    _outs = retrosheet_codes.play_formats.get_outs(res[0])

                    if _outs != -1:
                        self.outs_made = _outs if self.outs_made < _outs else self.outs_made
                    else:
                        self.outs_made -= 1 if self.outs_made > 0 else 0

                    print('\t{} >>>>>>> {} outs'.format(res[0], self.outs_made))



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
        self.away_team = None
        self.home_team = None
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

class team:
    def __init__(self, _id='', _name=''):
        self.team_id = ''
        self.team_name = ''
        self.league = None

class teams(Enum):
    '''
    Angels
    Astros
    Athletics
    Blue Jays
    Braves
    Brewers
    Cardinals
    Cubs
    D-backs
    Dodgers
    Giants
    Indians
    Mariners
    Marlins
    Mets
    Nationals
    Orioles
    Padres
    Phillies
    Pirates
    Rangers
    Rays
    Red Sox
    Reds
    Rockies
    Royals
    Tigers
    Twins
    White Sox
    Yankees
    '''