
from enum import Enum


class play_event_codes(Enum):
    wild_pitch = 'WP'
    passed_ball = 'PB'
    no_play = 'NP'
    intentional_walk = 'IW'
    walk = 'W'
    stolen_base = 'SB' #%
    stolen_base_1B = 'SB1'
    stolen_base_2B = 'SB2'
    stolen_base_3B = 'SB3'
    stolen_base_H = 'SBH'
    appeal_play = 'AP'
    batter_interference = 'BINT'
    bunt_line_drive = 'BL'
    batting_out_of_turn = 'BOOT'
    courtesy_batter = 'COUB'
    courtesy_fielder = 'COUF'
    courtesy_runner = 'COUR'
    fan_interference = 'FINT'
    foul = 'FL' #foul ball?
    interference = 'INT' #unspecified
    manager_review = 'MREV'
    no_double_play = 'NDP'
    obstruction = 'OBS'
    relay_throw = 'R' #$
    relay_throw_P = 'R1'
    relay_throw_C = 'R2'
    relay_throw_1B = 'R3'
    relay_throw_2B = 'R4'
    relay_throw_3B = 'R5'
    relay_throw_SS = 'R6'
    relay_throw_LF = 'R7'
    relay_throw_CF = 'R8'
    relay_throw_RF = 'R9'
    runner_interference = 'RINT'
    throw = 'TH' #%
    throw_to_1B = 'TH1'
    throw_to_2B = 'TH2'
    throw_to_3B = 'TH3'
    throw_to_H = 'THH'
    umpire_interference = 'UINT'
    umpire_reivew = 'UREV'
    defensive_interference = 'DI'
    base_runner_advance = 'OA' #unspecified by other codes
    unearned_run = 'UR'
    no_rbi_credited = 'NR'
    no_rbi_credited = 'NORBI'
    hit_by_pitch = 'HP'


class batted_ball_type(Enum):    
    bunt_ground_ball = 'BG'
    ground_ball = 'G'
    fly_ball = 'F'
    line_drive = 'L'


class fielding_error_event_codes(Enum):
    error = 'E' #$
    error_P = 'E1'
    error_C = 'E2'
    error_1B = 'E3'
    error_2B = 'E4'
    error_3B = 'E5'
    error_SS = 'E6'
    error_LF = 'E7'
    error_CF = 'E8'
    error_RF = 'E9'
    error_on_foul_fly = 'FLE' #$
    error_on_foul_fly_P = 'FLE1'
    error_on_foul_fly_C = 'FLE2'
    error_on_foul_fly_1B = 'FLE3'
    error_on_foul_fly_2B = 'FLE4'
    error_on_foul_fly_3B = 'FLE5'
    error_on_foul_fly_SS = 'FLE6'
    error_on_foul_fly_LF = 'FLE7'
    error_on_foul_fly_CF = 'FLE8'
    error_on_foul_fly_RF = 'FLE9'
    

class base_hit_event_codes(Enum):
    single = 'S' #$
    single_to_P = 'S1'
    single_to_C = 'S2'
    single_to_1B = 'S3'
    single_to_2B = 'S4'
    single_to_3B = 'S5'
    single_to_SS = 'S6'
    single_to_LF = 'S7'
    single_to_CF = 'S8'
    single_to_RF = 'S9'
    double = 'D' #$
    double_to_P = 'D1'
    double_to_C = 'D2'
    double_to_1B = 'D3'
    double_to_2B = 'D4'
    double_to_3B = 'D5'
    double_to_SS = 'D6'
    double_to_LF = 'D7'
    double_to_CF = 'D8'
    double_to_RF = 'D9'
    triple = 'T' #$
    triple_to_P = 'T1'
    triple_to_C = 'T2'
    triple_to_1B = 'T3'
    triple_to_2B = 'T4'
    triple_to_3B = 'T5'
    triple_to_SS = 'T6'
    triple_to_LF = 'T7'
    triple_to_CF = 'T8'
    triple_to_RF = 'T9'
    home_run = 'HR'
    #homerun = 'H' # alt code
    inside_the_park_home_run = 'IPHR'


class out_play_event_codes(Enum):
    bunt_popup = 'BP'
    sacrifice_fly = 'SF'
    force_out = 'FO'
    sacrifice_hit = 'SH'
    popup = 'P'
    strikeout = 'K'
    bunt_ground_ball_double_play = 'BGDP'
    bunt_popup_double_play = 'BPDP'
    runner_hit_by_batted_ball = 'BR'
    called_3rd_strike = 'C'
    double_play = 'DP' #unspecified
    triple_play = 'TP' #unspecified
    fly_ball_double_play = 'FDP'
    ground_ball_double_play = 'GDP'
    ground_ball_triple_play = 'GTP'
    infield_fly_rule = 'IF'
    lined_into_double_play = 'LDP'
    lined_into_triple_play = 'LTP'
    runner_passed = 'PASS'
    caught_stealing = 'CS' #%
    caught_stealing_1B = 'CS1' # I don't think this is possible
    caught_stealing_2B = 'CS2'
    caught_stealing_3B = 'CS3'
    caught_stealing_H = 'CSH'
    fielders_choice = 'FC' #$ - fielder first fielding the ball
    fielders_choice_P = 'FC1'
    fielders_choice_C = 'FC2'
    fielders_choice_1B = 'FC3'
    fielders_choice_2B = 'FC4'
    fielders_choice_3B = 'FC5'
    fielders_choice_SS = 'FC6'
    fielders_choice_LF = 'FC7'
    fielders_choice_CF = 'FC8'
    fielders_choice_RF = 'FC9'
    runner_put_out = 'X' # %X%($...$)
    runner_put_out_at_1B = 'X1'
    runner_put_out_at_2B = 'X2'
    runner_put_out_at_3B = 'X3'
    runner_put_out_at_H = 'XH'


class baserunner_advances(Enum):
    bbox_to_1B = 'B-1'
    bbox_to_2B = 'B-2'
    bbox_to_3B = 'B-3'
    bbox_to_H = 'B-H' #'IPHR' is more likely to be used here
    first_to_2B = '1-2'
    first_to_3B = '1-3'
    first_to_H = '1-H'
    second_to_3B = '2-3'
    second_to_H = '2-H'
    third_to_home = '3-H'
    

class location_codes(Enum):
    _1 = '1'
    _15 = '15'
    _13 = '13'
    _1S = '1S'
    _2 = '2'
    _2F = '2F'
    _25 = '25'
    _23 = '23'
    _25F = '25F'
    _23F = '23F'
    _3 = '3'
    _3F = '3F'
    _3S = '3S'
    _3D = '3D'
    _3DF = '3DF'
    _34 = '34'
    _34S = '34S'
    _34D = '34D'
    _4 = '4'
    _4S = '4S'
    _4M = '4M'
    _4D = '4D'
    _4MS = '4MS'
    _4MD = '4MD'
    _5 = '5'
    _5S = '5S'
    _5F = '5F'
    _5D = '5D'
    _5DF = '5DF'
    _56 = '56'
    _56S = '56S'
    _56D = '56D'
    _6 = '6'
    _6S = '6S'
    _6M = '6M'
    _6D = '6D'
    _6MS = '6MS'
    _6MD = '6MD'
    _7 = '7'
    _7S = '7S'
    _7L = '7L'
    _7D = '7D'
    _78 = '78'
    _7LS = '7LS'
    _7LD = '7LD'
    _78D = '78D'
    _78S = '78S'
    _7LSF = '7LSF'
    _7LF = '7LF'
    _7LDF = '7LDF'
    _78XD = '78XD'
    _8 = '8'
    _8D = '8D'
    _8S = '8S'
    _89 = '89'
    _8XD = '8XD'
    _89S = '89S'
    _89D = '89D'
    _89XD = '89XD'
    _9 = '9'
    _9S = '9S'
    _9D = '9D'
    _9L = '9L'
    _9LD = '9LD'
    _9LS = '9LS'
    _9LDF = '9LDF'
    _9LF = '9LF'
    _9LSF = '9LSF'


sorted_play_codes = list(play_event_codes)
sorted_play_codes.sort(key = lambda s: len(s.value), reverse=True)
sorted_out_play_codes = list(out_play_event_codes)
sorted_out_play_codes.sort(key = lambda s: len(s.value), reverse=True)
sorted_base_hit_codes = list(base_hit_event_codes)
sorted_base_hit_codes.sort(key = lambda s: len(s.value), reverse=True)
sorted_error_codes = list(fielding_error_event_codes)
sorted_error_codes.sort(key = lambda s: len(s.value), reverse=True)

sorted_batted_ball_types = list(batted_ball_type)
sorted_batted_ball_types.sort(key = lambda s: len(s.value), reverse=True)
sorted_baserunner_advances = list(baserunner_advances)
sorted_baserunner_advances.sort(key = lambda s: len(s.value), reverse=True)

sorted_locations = list(location_codes)
sorted_locations.sort(key = lambda s: len(s.value), reverse=True)

all_plays_sorted = []
all_plays_sorted += sorted_play_codes
all_plays_sorted += sorted_out_play_codes
all_plays_sorted += sorted_base_hit_codes
all_plays_sorted += sorted_error_codes
all_plays_sorted += sorted_batted_ball_types
all_plays_sorted += sorted_baserunner_advances
all_plays_sorted += sorted_locations
all_plays_sorted.sort(key = lambda s: len(s.value), reverse=True)



#@staticmethod
def get_event_code(_events, type=None):
    if _events == '': return None
    if type is None:
        for code in all_plays_sorted:
            if code.value in _events:
                return code
    elif type is play_event_codes:
        for code in sorted_play_codes:
            if code.value in _events:
                return code
    elif type is out_play_event_codes:
        for code in sorted_out_play_codes:
            if code.value in _events:
                return code
    elif type is base_hit_event_codes:
        for code in sorted_base_hit_codes:
            if code.value in _events:
                return code
    elif type is fielding_error_event_codes:
        for code in sorted_error_codes:
            if code.value in _events:
                return code
    elif type is location_codes:
        for code in sorted_locations:
            if code.value in _events:
                return code
    elif type is batted_ball_type:
        for code in batted_ball_type:
            if code.value in _events:
                return code
    else:
        return None
    

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