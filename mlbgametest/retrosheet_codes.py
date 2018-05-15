
from enum import Enum, unique
import itertools

@unique
class fielding_position_codes(Enum):
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
    #PH = 11
    #PR = 12
    @staticmethod
    def ntofpos(n):
        for pos in fielding_position_codes:
            if n == pos.value:
                return pos
    @staticmethod
    def getname(fp):
        if (fp in fielding_position_codes and fp is not fielding_position_codes.invalid):
            fpos_map = {
                fielding_position_codes.P:'Pitcher',
                fielding_position_codes.C:'Catcher',
                fielding_position_codes.B1:'First Base',
                fielding_position_codes.B2:'Second Base',
                fielding_position_codes.B3:'Third Base',
                fielding_position_codes.SS:'Shortstop',
                fielding_position_codes.LF:'Left Field',
                fielding_position_codes.CF:'Center Field',
                fielding_position_codes.RF:'Right Field',
                fielding_position_codes.DH:'Designated Hitter',
                #fielding_position_codes.PH:'Pinch Hitter',
                #fielding_position_codes.PR:'Pinch Runner',
            }
            return fpos_map[fp]
        else:
            return None

@unique
class notation_type(Enum):
    single_fielder = '$'
    several_fielders = '#' # can be one or more
    baserunner = '%'
    location = '@'
    batted_ball_type = '~'
    unknown_chr = '?'
    wildcard = '*' # can be one or more

    @staticmethod
    def get_char_to_type(_char):
        #return next((n for n in notation_type if n.value == _char), None)
        for n in notation_type:
            if n.value == _char:
                return n


@unique
class play_formats(Enum):
    '''
    Retrosheet uses a shorthand notation for fielders, baserunners. Let's try and use formatting to parse the event notation
    $       = fielder (Retrosheet)
    #       = variable number of fielders (this is my notation)
    %       = baserunner (Retrosheet)
    @       = location on field (this is my notation)
    ~       = batted ball type (this is my notation)
    ?       = unknown character (this is my notation)
    *       = unknown string (longer than 1 character)
    !       = if the string can only be at the very beginning of the play

    [..., ..., ...] = to explicitly specify event code possibilities. use ',' to separate. Can look for literals or notation. End list with a comma if you want to specify that these tokens might not exist.
    Any characters not recognized will be looked for literally, and not as codes.
    '''
    single = 'S$[/~,]'
    double = 'D$[/~,]'
    triple = 'T$[/~,]'
    error = '[$,]E$[/~,/TH,]'    
    out = '!#/[~,@,~@]'
    stolen_base_at = 'SB%'
    forceout = '#(%)/FO[/~,]'
    grounded_into_double_play = '#(%)#[(%),]/[~,]DP[/~,]'
    
    lined_into_double_play = '$(B)#(%)/LDP/~$'
    lined_into_triple_play = '$(B)#(%)#(%)/LTP/~$'
    batter_interference = 'C/[E2,E1,E3]'
    fielders_choice = 'FC$'
    error_on_foul_fly = 'FLE$'
    inside_the_park_home_run = '[HR,H]$' #/~@'
    baserunning_event_at = '+[SB,CS,PO]%'
    baserunning_error_event = '+E$'
    baserunning_event = '+[OA,PB,WP]'
    walk_event_at = '[IW,W]+[SB,CS,PO]%'
    walk_error_event = '[IW,W]+E$'
    walk_event = '[IW,W]+[PB,WP]'
    caught_stealing_at = 'CS%[($$),]'
    caught_stealing_error = 'CS%($E$)'
    picked_off_at = 'PO%($$)'
    pick_off_error = 'PO%(E$)'
    picked_off_caught_stealing = 'POCS%(#)'
    strikeout_fielding_play = 'K#'
    
    baserunning_advances = '[.,;]%-%'

    walk = 'W'
    intentional_walk = 'IW'
    wild_pitch = 'WP'
    strikeout = 'K'
    hit_by_pitch = 'HP'
    home_run = 'HR'
    no_play = 'NP'
    passed_ball = 'PB'
    defensive_indifference = 'DI'
    out_ambiguous = 'OA'
    ground_rule_double = 'DGR'
    stolen_base = 'SB'
    balk = 'BK'
    line_drive_bunt = 'BL'
    double_play = 'DP'

    putout_baserunner = '%X%(#[/TH,])'
    strikeout_error_event = 'K+E$[/TH,]' #maybe not necessary to specify baserunning events
    
    #class play(object):
    #    def __init__(self):
    #        self.fielders = []
    #        self.baserunners = []
    #        self.location = None
    #        self.batted_ball = None


    @staticmethod
    def matches_format(_events):
        '''
        Will return multiple matches if more than one is found.
        '''
    
        def is_code_at_str_idx(code, _string, _start_index):
            return _string[_start_index:_start_index+len(code)] == code

        def is_notation_type(ntype, _str, _start_index=0):
            #print('|> {} "{}" [{}]'.format(ntype, _str, _start_index))
            if ntype is notation_type.single_fielder:
                fielders = list(str(f.value) for f in fielding_position_codes)
                for f in fielders:
                    if (is_code_at_str_idx(f, _str, _start_index)):
                        return len(f)
            elif ntype is notation_type.several_fielders:
                fielders = list(str(f.value) for f in fielding_position_codes)
                n_itr = -1
                for n, f in enumerate(_str[_start_index:]):
                    bFound = False
                    for fielder in fielders:
                        if (is_code_at_str_idx(fielder, _str, _start_index + n)):
                            bFound = True
                            n_itr = n + 1
                            break
                        else:
                            bFound = False
                    if (bFound == False):
                        if (n == 0): # first item was invalid, need to return -1 to indicate no matches
                            return -1
                        return n_itr
                return n_itr
            elif ntype is notation_type.baserunner:
                runners = list(br.value for br in baserunner_codes)
                for r in runners:
                    if (is_code_at_str_idx(r, _str, _start_index)):
                        return len(r)
            elif ntype is notation_type.location:
                for loc in sorted_locations:                    
                    if (is_code_at_str_idx(loc.value, _str, _start_index)):
                        return len(loc.value)
            elif ntype is notation_type.batted_ball_type:
                for bbt in sorted_batted_ball_types:
                    if (is_code_at_str_idx(bbt.value, _str, _start_index)):
                        return len(bbt.value)
            elif ntype is notation_type.unknown_chr:
                return 1 # doesn't matter
            elif ntype is notation_type.wildcard:
                return 0 # might need special return value

            return -1


        def compare_string_to_format(_string, _frmt): 
            for i, _ in enumerate(_string):
                bAtBegin = _frmt[0] == '!'
                nbegin = -1
                nend = -1
                s = _string[i:] # need to step through the string since the match could be anywhere
                bFound = False
                _string_itr = 0
                match_string = '' # sequence of characters that matches the format string
                for j, tkn in enumerate(_frmt):
                    if j == 0 and bAtBegin:
                        continue
                    if _string_itr < len(s):
                        cand_char = s[_string_itr]
                        ntype = notation_type.get_char_to_type(tkn)
                        if ntype is not None:
                            #print('tkn="{}"'.format(tkn))
                            #print('ntype={}'.format(ntype._name_))
                            #print('looking at "{}" in "{}"'.format(cand_char, s))
                            #print('comparing against type: {}[{}] in {}'.format(ntype.value, j, _frmt))
                            notatlen = is_notation_type(ntype, s, _string_itr)
                            if notatlen != -1:
                                #print('MATCH! notation comparision: "{}"[{}] matches with "{}"[{}]. "{}" is of type: {} ({})'.format(s, _string_itr, _frmt, j, s[_string_itr:notatlen + _string_itr], ntype._name_, tkn))
                                bFound = True
                                if nbegin == -1:
                                    nbegin = _string_itr + i
                                _string_itr += notatlen
                                match_string = s[:_string_itr]
                            else:
                                #print('FAILURE! notation comparision: "{}"[{}] does not match with "{}"[{}]. "{}" is NOT of type: {} ({})'.format(s, _string_itr, _frmt, j, cand_char, ntype._name_, tkn))
                                bFound = False
                                nend =  _string_itr + i
                                break
                        elif ntype == None: # char literal
                            if tkn == cand_char:
                                #print('MATCH! char="{} \t|\t literal comparison: "{}"[{}] matches with "{}"[{}]."'.format(tkn, s, _string_itr, _frmt, j))
                                bFound = True                                
                                if nbegin == -1:
                                    nbegin =  _string_itr + i
                                _string_itr += 1
                                match_string = s[:_string_itr]
                            else:
                                #print('FAILURE! "{}" != "{}" \t|\t literal comparison: "{}"[{}] failed to match with "{}"[{}].'.format(cand_char, tkn, s, _string_itr, _frmt, j))
                                bFound = False
                                nend =  _string_itr + i
                                break
                        #print('_string_itr = {}'.format(_string_itr))
                        nend =  _string_itr + i
                    else:
                        #print('reached past end of "{}". Format "{}" is longer than event string.'.format(s, _frmt))
                        nend =  _string_itr + i
                        bFound = False
                # end of loop:
                if bFound is True:
                    #print('"{}" seems to match with "{}" in "{}"'.format(_frmt, match_string, s))
                    return match_string, nbegin, nend
                elif bAtBegin:
                    break
            return '', -1, -1

        def enumerate_bracket_options(format, _obrkt='[', _cbrkt=']'):
            if _obrkt in format and _cbrkt in format:
                option_strings = []
                brkt_splits = []
                last_n = 0
                for n, chr in enumerate(format):
                    if chr == _obrkt or chr == _cbrkt:
                        brkt_splits.append(format[last_n if format[last_n-1] != _obrkt else last_n-1:n if chr != _cbrkt else n+1])
                        last_n = n + 1
                if len(format[last_n:]) > 0:
                    brkt_splits.append(format[last_n:])
                list_option_lists = []
                for split in brkt_splits:
                    if (_obrkt in split and _cbrkt in split):
                        list_option_lists.append(split.replace(_obrkt,'').replace(_cbrkt,'').split(','))
                for i, split in enumerate(brkt_splits):
                    brkt_splits[i] = split.strip()
                brkt_splits = filter(None, brkt_splits)
                where_brkts = [n for n, _ in enumerate(brkt_splits) if (_obrkt in _ and _cbrkt in _)]
                options_list = list(itertools.product(*list_option_lists))                
                for options in options_list:
                    #print(options)
                    new_format = ''
                    option_itr = 0
                    for i, split in enumerate(brkt_splits):
                        if _obrkt not in split and _cbrkt not in split:
                            new_format += split
                        else:
                            #print(options, option_itr)
                            new_format += options[option_itr]
                            option_itr += 1
                    option_strings.append(new_format)
                return option_strings
            else:
                return []



        matches = []
        formats = list(play_formats)
        formats.sort(key = lambda s: len(s.value), reverse=False)
        format_res = []
        for _frmt in formats:
            format = _frmt.value
            #print('evaluating "{}"'.format(format))
            if '[' in format and ']' in format:                
                options = enumerate_bracket_options(format)
                options.sort(key = lambda s: len(s), reverse=False)
                for opt_str in options:
                    #print('evaluating option "{}" in format: "{}" ({})'.format(opt_str, _frmt.value, _frmt._name_))
                    match_string, begin, end = compare_string_to_format(_events, opt_str)
                    if match_string != '':
                        #print('Detected: {} "{}" in play: {} @ ({},{})="{}".'.format(_frmt._name_, opt_str, _events, begin, end, _events[begin:end]))
                        format_res.append((_frmt, opt_str, match_string, (begin, end)))
            else:
                match_string, begin, end = compare_string_to_format(_events, format)
                if match_string != '':
                    #print('Detected: {} "{}" in play: {} @ ({},{})="{}".'.format(_frmt._name_, format, _events, begin, end, _events[begin:end]))
                    format_res.append((_frmt, format, match_string, (begin, end)))
        if len(format_res) > 0:
            matches += format_res

        if len(matches) == 0:
            print('Could not find a matching play type for: {} !'.format(_events))
            for code in play_event_codes:
                idx = _events.find(code.value)
                if idx != -1:
                    #print('found "{}" in "{} @ ({},{})="{}""'.format(code._name_, _events, idx, len(code.value), _events[idx:len(code.value)]))
                    matches.append((code, '', code.value, (idx, len(code.value))))
            for code in out_play_event_codes:
                idx = _events.find(code.value)
                if idx != -1:
                    #print('found "{}" in "{}"'.format(code._name_, _events, idx, len(code.value), _events[idx:len(code.value)]))
                    matches.append((code, '', code.value, (idx, len(code.value))))
        else:            
            #print('matching formats for "{}":'.format(_events))
            #for match in matches: print('{}'.format(match))
            duplicates = [_match for match in matches for _match in matches if _match[2] in match[2] and _match is not match]
            matches = [m for m in matches if m not in duplicates]

            #remove format matches that overlap one another
            if len(matches) > 1:
                coords = [m[3] for m in matches]
                for r in coords:
                    rb, re = r
                    xs = set(range(rb,re))
                    for n, y in enumerate(coords):
                        if y is not r:
                            yb, ye = y
                            xy = xs.intersection(range(yb,ye))
                            if len(xy) > 0:
                                #print('{} ^ {} = {} '.format(xs, y, xy))
                                #print('{} {}'.format(_events[rb:re], _events[yb:ye]))
                                matches = [m for m in matches if m[3] != y]
                                coords.remove(y)
                                break
            
        print('matching formats for "{}":'.format(_events))
        for match in matches: print('{}'.format(match))

        if len(matches) < 1:
            print('COULD NOT FIND A MATCH!!!')

        return matches


@unique
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
    balk = 'BK'


@unique
class batted_ball_type(Enum):
    bunt_grounder = 'BG'
    bunt_popup = 'BP'
    popup = 'P'
    ground_ball = 'G'
    fly_ball = 'F'
    line_drive = 'L'

@unique
class out_play_event_codes(Enum):
    bunt_popup = 'BP'
    sacrifice_fly = 'SF'
    force_out = 'FO'
    sacrifice_hit = 'SH'
    #popup = 'P'
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
    
@unique
class baserunner_codes(Enum):
    '''
    These are usually surrounded by () for outs
    '''
    batter = 'B'
    runner_from_1B = '1'
    runner_from_2B = '2'
    runner_from_3B = '3'
    home_plate = 'H'

@unique
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
#sorted_base_hit_codes = list(base_hit_event_codes)
#sorted_base_hit_codes.sort(key = lambda s: len(s.value), reverse=True)
#sorted_error_codes = list(fielding_error_event_codes)
#sorted_error_codes.sort(key = lambda s: len(s.value), reverse=True)

sorted_batted_ball_types = list(batted_ball_type)
sorted_batted_ball_types.sort(key = lambda s: len(s.value), reverse=True)
#sorted_baserunner_advances = list(baserunner_advances)
#sorted_baserunner_advances.sort(key = lambda s: len(s.value), reverse=True)

sorted_locations = list(location_codes)
sorted_locations.sort(key = lambda s: len(s.value), reverse=True)

all_plays_sorted = []
all_plays_sorted += sorted_play_codes
all_plays_sorted += sorted_out_play_codes
#all_plays_sorted += sorted_base_hit_codes
#all_plays_sorted += sorted_error_codes
all_plays_sorted += sorted_batted_ball_types
#all_plays_sorted += sorted_baserunner_advances
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
    

@unique
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

@unique
class pitchres_mod(Enum):
    # these are modifiers that come after the pitch result
    catcher_pickoff = '+'
    catcher_blocked_pitch = '*'
    runner_going = '>'