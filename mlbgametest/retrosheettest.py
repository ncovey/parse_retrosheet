
import sys
import os
import time
from parse_retrosheet import *
from parse_retrosheet import record_type as rt

'''
I want to see if it is possible to compile information about catcher performances to help quantify their defensive performance. This is a relatively uncharted area of research, and is a notoriously difficult problem.
cERA (catcher ERA) is interesting, but it lumps together all of the pitchers instead of how each pitcher performed in a particular battery with that catcher.
In that vein, I would like to gather all of the pitcher-catcher batteries and calculate each one's performance. While catchers tend to catch most, if not all, games in a season for a club, sometimes for a full 9 innings, I think it can be helpful to look at how every battery performed from year-to-year.
We can evaluate many things specific to each battery (ERA being one of them), as well as framing numbers, CS rate, take-off rate, passed balls, wild pitches, pitch type %, walk rate, strikeout rate, etc.
We can then look at the battery's performace to the pitcher's above/below overall performance AND the battery's performance to the catcher's overall performance (maybe for that season, or from year to year).
The underlying theory to doing this analysis is that good catchers are more likely to help more pitchers succeed, while poor catchers can contribute to poor pitching performances. Hopefully, large sample sizes will offset outside factors enough.
Obviously, you can't blame the catcher if a pitcher under-performed with him for that year. However, if you look at how ALL pitchers performed with that catcher for his career, and see that, on average, they under-performed--maybe we can say, at least, the catcher is not helping in those pitchers under-performing.
For example, I noticed that Kershaw's ERA when A.J. Ellis caught him is notably lower than after Ellis was traded to the Phillies in 2016. Of course, other factors such as Kershaw's back injury may have had a role in that, as well as what appears to be philosophy change from inducing weak contact instead of strikeouts (possibly due to a loss in FB velocity).
We can't look at factors like team ERA from year to year because teams tend to move pitchers around via trades and transactions so often. Usually a team's rotation and bullpen can be very different from year to year. However, in cases where teams make little to no change to their pitching staff, looking at battery statistics is independent of those factors.

# 1) keep track of the number of outs (every 3 outs is one inning) the pitcher has gotten
# 2) then multiply by number of earned runs divided by 9 to get ERA with this catcher (subset of cERA)
# 3) Determine the pitcher's ERA on the season, and subtract the value determined above to get the cERA-battery differential for the battery on the season
# 4) When you have the cERA-battery-differential, calculate a mean average weighted by innings caught between all of catcher's batteries to get a single number for how much, on average, a catcher may have improved his pitcher's ERA
# step (3) might also be performed by looking at all cERA-battery values, and getting a non-innings-caught-weighted mean average (if we add weight, this would be the same as the pitcher's ERA on the season) for all qualified catchers who caught an arbitrary minimum number of innings, and calculating the differential based upon that value.
# step (3) might also be calculated by determining the *median*-differential of of all cERA-battery values. We can then look at the weighted mean of all batteries in step (4)

^^ the above might also be interesting to do with balls/strikes called to see if maybe particular catchers have a higher rate of balls/strikes called in their batteries. We can then compare this to framing metrics (pitches out of the zone called strikes, and in the zone called balls). 
We can then qualify framing metrics (which I think is a horrible way to evaluate catchers overall, despite how important it can be) and see that even if a catcher does not get favorable calls, if maybe they still have a high rate compared to other catchers of called strikes (most likely because those pitches were ACTUALLY strikes).
If pitch framing is as important a metric as one might think, then we should see that called balls and strikes

'''

EVENT_DIR = '2017eve/'

dict_catchers = {}

class innings_val():
    def __init__(self, innings, outs):
        self.innings = innings
        self.outs = outs
    @staticmethod
    def from_total_outs(total_outs):
        return innings_val(int(total_outs / 3), total_outs % 3)
    def to_float(self):
        return float(self.innings) + (float(self.outs)/3.0)
    def to_outs(self):
        return (int(self.innings) * 3) + int(self.outs)
    def is_valid(self):
        return self.innings >= 0 and self.outs >= 0
    def __sub__(self, rhs):
        return self.from_total_outs(self.to_outs() - rhs.to_outs())
    def __add__(self, rhs):
        return self.from_total_outs(self.to_outs() + rhs.to_outs())

class pitcher_perf():
    '''
    the 'inning_end' parameter is the point in the game in which the pitcher stopped pitching. If a starting pitcher goes into the 5th and is pulled after 2 outs, then
    that pitcher has pitched 4.2 innings. Provide innings_val(5, 2) as the inning_end value
    '''
    def __init__(self, is_home, player_id, inningsval=None, earned_runs=-1):
        self.is_home = is_home
        self.player_id = player_id
        self.inning_start = None
        self.inning_end = None
        self.innings_pitched = inningsval
        self.earned_runs = earned_runs
    def set_ip(self, startinn, endinn, startouts=0, endouts=0):
        self.inning_start = innings_val(startinn, startouts)
        self.inning_end = innings_val(endinn, endouts)
        self.innings_pitched = self.inning_end - innings_val(self.inning_start.innings if self.inning_start.innings != 0 else 1, self.inning_start.outs) #innings_val(endinn - (1 if startinn == 0 else 0), endouts) - innings_val(startinn, startouts)
        return self.innings_pitched
    def set_ip(self):
        self.innings_pitched = self.inning_end - innings_val(self.inning_start.innings if self.inning_start.innings != 0 else 1, self.inning_start.outs)
        return self.innings_pitched

def parse_game_for_batteries(game):
    
    home_sp_perf = None
    home_c = None
    away_sp_perf = None
    away_c = None
    for starter in game.starters_home:
        if (starter.start_field_pos == fpos.C):
            home_c = starter.player_id
        elif (starter.start_field_pos == fpos.P):
            home_sp_perf = pitcher_perf(True, starter.player_id)
            home_sp_perf.inning_start = innings_val(0, 0)
    for starter in game.starters_away:
        if (starter.start_field_pos == fpos.C):
            away_c = starter.player_id
        elif (starter.start_field_pos == fpos.P):
            away_sp_perf = pitcher_perf(False, starter.player_id)
            away_sp_perf.inning_start = innings_val(0, 0)

    def add_battery_to_dict(catcher, game, pperf):
        for dat in game.data:
            if pperf.player_id == dat.pitcher:
                pperf.earned_runs = dat.earned_runs
                break
        if pperf.earned_runs != -1:
            pperf.inning_end = innings_val(inning, outs)
            pperf.set_ip()
            #print('catcher {} caught {}.{} innings for pitcher {} [{}]'.
            #      format(catcher, pperf.innings_pitched.innings, pperf.innings_pitched.outs, pperf.player_id, 'home' if play.is_home else 'away'))
            if pperf.innings_pitched is not None and pperf.innings_pitched.is_valid():
                era = 'infinite'
                if pperf.innings_pitched.to_float() != 0:
                    era = (float(pperf.earned_runs)/pperf.innings_pitched.to_float()) * 9.0
                #print('\t{} is charged with {} earned runs (determined at end of game) over {}.{} innings pitched (ERA = {})'
                #      .format(pperf.player_id, pperf.earned_runs, pperf.innings_pitched.innings, pperf.innings_pitched.outs, "{0:.2f}".format(era) if era != 'infinite' else era))

                batteries = dict_catchers.get(catcher)
                if batteries is None:
                    dict_catchers[catcher] = { pperf.player_id : { game : pperf } }
                    batteries = dict_catchers.get(catcher)
                #batteries[pperf.player_id][game] = {}
                pitcher = batteries.get(pperf.player_id)
                if pitcher is None:
                    batteries[pperf.player_id] = { game : pperf }
                    pitcher = batteries.get(pperf.player_id)
                pitcher[game] = pperf # maybe append a list of other stats later when I can extract more data (earned runs, walks, etc.)
        else:
            print('COULD NOT FIND PITCHER {} IN DATA FIELDS!!!'.format(pitcher))


    outs = 0
    inning = 0
    is_home = None
    catcher = None
    pperf = None

    for n, play in enumerate(game.plays):
        if (play.is_home != is_home) and play._type != rt.sub.value:
            if (outs < 3 and is_home != None):
                print('Warning! -less- than 3 outs detected!')
                #raise(Exception('Warning! -less- than 3 outs detected!'))
            elif (outs > 3 and is_home != None):
                print('Warning! +more+ than 3 outs detected!')
                #raise(Exception('Warning! +more+ than 3 outs detected!'))
            outs = 0
            is_home = play.is_home
        if (hasattr(play, 'inning') and play.inning != inning):
            inning = int(play.inning)
        if play._type == rt.play.value:
            #print ('\n=== {} of the {} ==='.format('bottom' if is_home else 'top', inning))
            play.parse_play_results()
            #print('{}'.format(','.join(play._values)))
            if (play.outs_made != -1):
                outs += play.outs_made
                #print('+{} outs; total outs in inning:    [{}]'.format(play.outs_made, outs))
        if play._type == rt.sub.value:
            #print('{} replaces {} for {} team, batting {}, with {} outs left in the inning.'
            #      .format(play.player_id, fpos.getname(play.sub_field_pos), 'home' if is_home else 'away', play.batting_order, outs))
            if play.sub_field_pos == fpos.P:
                catcher = home_c if is_home else away_c
                pperf = home_sp_perf if is_home else away_sp_perf
                
                add_battery_to_dict(catcher, game, pperf)

                #### set new pitcher ####
                if (is_home):
                    home_sp_perf = pitcher_perf(is_home, play.player_id)
                    home_sp_perf.inning_start = innings_val(inning, outs)
                else:
                    away_sp_perf = pitcher_perf(is_home, play.player_id)
                    away_sp_perf.inning_start = innings_val(inning, outs)

                   
            # this is hard right now
            if play.sub_field_pos == fpos.C:
                catcher = home_c if is_home else away_c
            #    pperf = home_sp_perf if is_home else away_sp_perf
                print('catcher {} for the {} team replaced by catcher {}'.format(catcher, 'home' if is_home else 'away', play.player_id))
                
            #    batteries = dict_catchers.get(catcher)
            #    if batteries is None:
            #        dict_catchers[catcher] = {}
            #        batteries = dict_catchers.get(catcher)                        
            #    batteries[pperf.player_id] = {game : pperf} # maybe append a list of other stats later when I can extract more data (earned runs, walks, etc.)
            #    #### set new catcher ####                
            #    if is_home == True: home_c = play.player_id
            #    else: away_c = play.player_id
            #    #### we need to create a new pitcher record because the battery is different ####
            #    #pperf = pitcher_perf(is_home, play.player_id)
            #    pperf.inning_start = innings_val(inning, outs)
    
    # add the last batteries at end of game:
    add_battery_to_dict(home_c, game, home_sp_perf)
    add_battery_to_dict(away_c, game, away_sp_perf)
            
            
    if outs != 3:
        print('game did not end with 3 outs???')

def run_tests():    
    testcases = [
    ["S1", 0],
    ["64(2)4(1)3/GTP", 3],
    ["34/SH.2-3", 1],
    ["K+WP.2-3;B-1", 0],
    ["K+WP.2-3;1-2", 1],
    ["S7/G/MREV.2XH(72)", 1],
    ["53/SH/BG-.1-2", 1],
    ["K+E2/TH.2-3;B-1", 0],
    ["9/F9LF", 1],
    ["S8/L.2-H;1-3", 0],
    ["8!/F+", 1],
    ["7/L/TP.2X2(74);1X1(43)", 3],
    ["OA.2-3(E2/TH);1-2(TH)", 0],
    ["K+SB3.2-H(UR)(E2/TH3);1-2", 1],
    ["OA.3-H(UR)(E2)(NR);1-2", 0],
    ["OA.3-H(UR)(E2/TH)(NR);2-H(UR)(NR);1-2", 0],
    ["OA.1-2(E2/TH)", 0],
    ["OA.2-3(E2/TH);1-2(TH)", 0],
    ["OA.3-H(E2/TH);2-H(UR);1-2", 0],
    ["W+OA.1-3(E2/TH)", 0],
    ["OA.1-2(E2/TH)", 0],
    ["53", 1],
    ["43-/G", 1],
    ["PO2(256)", 1],
    ["K+SB2.1-3(E2/TH)", 1],
    ["K+PO2(E2).2-3", 1],
    ]
    for test in testcases:
        st, o = test[0], test[1]
        begin_time = time.time()
        results = retrosheet_codes.matches_format(st)
        print ('total time to find matching formats: {}'.format(time.time() - begin_time))
        outs = 0;
        print('{}'.format(test))
        for res in results:
            _out = retrosheet_codes.get_outs(res[0])
            if outs < 3:
                outs += _out
            print('\t{} ({}): out = {}'.format(res[2], res[1], _out))
        print('outs detected: {}\n'.format(outs))
        if outs == -1: outs = 0
        if outs != o:
            print("FAILED. Expected {} outs".format(o))
            return False
    # all tests passed        
    return True

def innings_test():
    p1 = pitcher_perf(True, 'dummy')
    p1.inning_start = innings_val(0, 0)
    p1.inning_end = innings_val(5, 2)
    p1.set_ip()
    print('{}.{}'.format(p1.innings_pitched.innings, p1.innings_pitched.outs))

def main():

    #innings_test()
    #assert(run_tests())

    eventdata = {}
    rosdata = {}

    begin_time = time.time()
    for filename in os.listdir(EVENT_DIR):
        #if ('.EVN' in filename or '.EVA' in filename):
        if ('SDN.EVN' in filename): # for debug
            eventdata[filename] = open(EVENT_DIR + filename, 'r')
        #elif ('.ROS' in filename):
        #    rosdata[filename] = open(EVENT_DIR + filename, 'r')
    
    print ('time to read in files: {}'.format(time.time() - begin_time))
        
    game_records = {}

    game_itr = None
    
    begin_time = time.time()
    for team, events in eventdata.iteritems():
        for line in events:
            line = line.strip('\n')
            #print (line)
            tokens = line.split(',')
            #print(tokens)
            tk = tokens[0]
            if (tk == rt.id.value):
                id = tokens[1]
                if (game_records.get(id) is None):
                    game_records[id] = game_record()
                    game_itr = game_records.get(id)
                    game_itr.id = id
            elif game_itr is not None:
                game_itr.add(tokens)

    print ('time to parse event data: {}'.format(time.time() - begin_time))
        
    begin_time = time.time()
    for id, game in game_records.iteritems():

        parse_game_for_batteries(game)

        #break #debug to just analyze one game
        #for sub in game.substitutions:
        #    if (sub.s)

    # debug print:
    for catcher, batteries in dict_catchers.iteritems():
        total_innings = innings_val(0, 0)
        for pitcher, game in batteries.iteritems():
            for game, perf in game.iteritems():
                print('{} | {} | innings: {}.{} | earned runs: {}'.format(catcher, pitcher, perf.innings_pitched.innings, perf.innings_pitched.outs, perf.earned_runs))
                total_innings += perf.innings_pitched
        #total = innings_val.from_total_outs(catcher_innings)
        print('{} caught {}.{} innings total.'.format(catcher, total_innings.innings, int(total_innings.outs)))
    #print('{}'.format(dict_catchers))


    print ('time to compile catcher and pitcher records: {}'.format(time.time() - begin_time))

    return

if __name__=="__main__":
    main()
        