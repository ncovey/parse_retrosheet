
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
        self.play_formats = []
        #self.parse_play_results()


    def parse_play_results(self):
        num_plays = 0
        #results = retrosheet_codes.play_formats.matches_format("S8/L.2-H;1-3")
        #results = retrosheet_codes.play_formats.matches_format("9/F9LF")
        #results = retrosheet_codes.play_formats.matches_format("K+E2/TH.2-3;B-1")
        results = retrosheet_codes.play_formats.matches_format(self.play_results)
        
        if len(results) > 0:
            for res in results:
                self.play_formats.append(res[0])
                #print('"{}" - {} ({})'.format(self.play_results, res[0], res[1]))

                if \
                res[0] == retrosheet_codes.play_formats.single or \
                res[0] == retrosheet_codes.play_formats.double or \
                res[0] == retrosheet_codes.play_formats.triple or \
                res[0] == retrosheet_codes.play_formats.home_run or \
                res[0] == retrosheet_codes.play_formats.inside_the_park_home_run:
                    self.base_hit = True

                if \
                res[0] == retrosheet_codes.play_formats.out or \
                res[0] == retrosheet_codes.play_formats.forceout or \
                res[0] == retrosheet_codes.play_formats.caught_stealing_at or \
                res[0] == retrosheet_codes.play_formats.picked_off_at or \
                res[0] == retrosheet_codes.play_formats.picked_off_caught_stealing or \
                res[0] == retrosheet_codes.play_formats.strikeout_fielding_play or \
                res[0] == retrosheet_codes.play_formats.strikeout or \
                res[0] == retrosheet_codes.play_formats.out_ambiguous or \
                res[0] == retrosheet_codes.play_formats.line_drive_bunt or \
                res[0] == retrosheet_codes.play_formats.putout_baserunner:
                    self.outs_made = 1 if self.outs_made < 1 else self.outs_made
                elif \
                res[0] == retrosheet_codes.play_formats.double_play or \
                res[0] == retrosheet_codes.play_formats.grounded_into_double_play or \
                res[0] == retrosheet_codes.play_formats.lined_into_double_play:
                    self.outs_made = 2 if self.outs_made < 2 else self.outs_made
                elif \
                res[0] == retrosheet_codes.play_formats.lined_into_triple_play:
                    self.outs_made = 3 if self.outs_made < 3 else self.outs_made

                if \
                res[0] == retrosheet_codes.play_formats.error_on_foul_fly or \
                res[0] == retrosheet_codes.play_formats.pick_off_error or \
                res[0] == retrosheet_codes.play_formats.strikeout_error_event or \
                res[0] == retrosheet_codes.play_formats.walk_error_event:
                    self.outs_made -= 1 if self.outs_made > 0 else 0 #????? how am I supposed to know how many outs??
                    
                print('\t{} >>>>>>> {} outs'.format(res[0], self.outs_made))

            if self.base_hit == True and not any(res[0] == retrosheet_codes.play_formats.putout_baserunner for res in results) :
                self.outs_made = -1


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

