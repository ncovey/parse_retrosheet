
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

def parse_game_for_batteries(game):
    
    #starting_pitcher_home = None
    #starting_catcher_home = None
    #starting_pitcher_away = None
    #starting_catcher_away = None
    #for starter in game.starters:
    #    if (starter.start_field_pos == fpos.C):
    #        if (starter.is_home):                
    #            starting_catcher_home = starter.player_id
    #        else:
    #            starting_catcher_away = starter.player_id
    #    elif (starter.start_field_pos == fpos.P):
    #        if (starter.is_home):
    #            starting_pitcher_home = starter.player_id
    #        else:
    #            starting_pitcher_away = starter.player_id

    #batteries = dict_catchers.get(catcher)
    #if batteries is None:
    #    dict_catchers[catcher] = {}
    #    batteries = dict_catchers.get(catcher)
    #pitcher_appearances = batteries.get(pitcher)
    #if pitcher_appearances is None:
    #    batteries[pitcher] = []
    #    pitcher_appearances = batteries.get(pitcher)

    outs = 0
    inning = 0
    is_home = None

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
            inning = play.inning
        if play._type == rt.play.value:
            print ('\n=== {} of the {} ==='.format('bottom' if play.is_home else 'top', inning))            
            play.parse_play_results()
            if (play.outs_made != -1):
                outs += play.outs_made
                print('total outs in inning:    [{}]'.format(play.outs_made, outs))
            #else:
            #    print('Warning! could not determine number of outs made!')
        if play._type == rt.sub.value:
            print('{} replaces {} for {} team, batting {}, with {} outs left in the inning.'
                  .format(play.player_id, fpos.getname(play.sub_field_pos), 'home' if play.is_home else 'away', play.batting_order, outs))
            #if play.sub_field_pos == fpos.P:
            #    print('catcher {} caught {}.{} innings for pitcher {}'.format(catcher, inning, outs, pitcher))
            #    pitcher_appearances.append((game, float(str(inning)+'.'+str(outs)), [])) # maybe append a list of other stats later when I can extract more data (earned runs, walks, etc.)
            #    pitcher = play.player_id               
            #    pitcher_appearances = batteries.get(pitcher)
            #    if pitcher_appearances is None:
            #        batteries[pitcher] = []
            #        pitcher_appearances = batteries.get(pitcher)
            #if play.sub_field_pos == fpos.C:
            #    print('catcher replaced')
            #    catcher = play.player_id
            #    batteries = dict_catchers.get(catcher)
            #    if batteries is None:
            #        dict_catchers[catcher] = {}
            #        batteries = dict_catchers.get(catcher)

            #add_pitcher_to_catcher_dict(catcher, pitcher, None)


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

def main():

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
    print ('time to compile catcher and pitcher records: {}'.format(time.time() - begin_time))

    return

if __name__=="__main__":
    main()
        