
from enum import Enum


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
    error_P = 'E1'
    error_C = 'E2'
    error_1B = 'E3'
    error_2B = 'E4'
    error_3B = 'E5'
    error_SS = 'E6'
    error_LF = 'E7'
    error_CF = 'E8'
    error_RF = 'E9'
    strikeout = 'K'
    wild_pitch = 'WP'
    passed_ball = 'PB'
    intentional_walk = 'IW'
    walk = 'W'
    stolen_base = 'SB'
    appeal_play = 'AP'
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
    triple_play = 'TP' #unspecified
    umpire_interference = 'UINT'
    umpire_reivew = 'UREV'
    defensive_interference = 'DI'
    base_runner_advance = 'OA' #unspecified by other codes
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
