
import os
from parse_retrosheets import *
from parse_retrosheets import record_type as rt

'''
I want to see if it is possible to compile information about catcher performances to help quantify their defensive performance. This is a relatively uncharted area of research, and is a notoriously difficult problem.
cERA (catcher ERA) is interesting, but I feel it does not really indicate how a pitcher performed with that particular battery with that catcher.
In that vein, I would like to gather all of the pitcher-catcher batteries and calculate each one's performance. While catchers tend to catch most, if not all, games in a season for a club, sometimes for a full 9 innings, I think it can be helpful to look at how every battery performed from year-to-year.
We can evaluate many things specific to each battery (ERA being one of them), as well as framing numbers, CS rate, take-off rate, passed balls, wild pitches, pitch type %, walk rate, strikeout rate, etc.
We can then look at the battery's performace to the pitcher's above/below overall performance AND the battery's performance to the catcher's overall performance (maybe for that season, or from year to year).
The underlying theory to doing this analysis is that good catchers are more likely to help more pitchers succeed, while poor catchers can contribute to poor pitching performances. Hopefully, large sample sizes will offset outside factors enough.
Obviously, you can't blame the catcher if a pitcher under-performed with him for that year. However, if you look at how ALL pitchers performed with that catcher for his career, and see that, on average, they under-performed--maybe we can say, at least, the catcher is not helping in those pitchers under-performing.
For example, I noticed that Kershaw's ERA when A.J. Ellis caught him is notably lower than after Ellis was traded to the Phillies in 2016. Of course, other factors such as Kershaw's back injury may have had a role in that, as well as what appears to be philosophy change from inducing weak contact instead of strikeouts (possibly due to a loss in FB velocity).
We can't look at factors like team ERA from year to year because teams tend to move pitchers around via trades and transactions so often. Usually a team's rotation and bullpen can be very different from year to year. However, in cases where teams make little to no change to their pitching staff, looking at battery statistics is independent of those factors.

The two main components are: (1) battery combinations and (2) determining relative performance.
We want to see innings caught for that battery as a well as a combination of results such as battery ERA.
We want evaluate two things to differentiate between pitcher and catcher performance

'''

EVENT_DIR = '2017eve/'


def main():

    eventdata = {}
    rosdata = {}

    for filename in os.listdir(EVENT_DIR):
        if ('2017SDN.EVN' in filename):
            eventdata[filename] = open(EVENT_DIR + filename, 'r')
        #elif ('.ROS' in filename):
        #    rosdata[filename] = open(EVENT_DIR + filename, 'r')

    game_records = []

    game_itr = None

    for team, events in eventdata.iteritems():
        for line in events:
            line = line.strip('\n')
            #print (line)
            tokens = line.split(',')
            #print(tokens)
            tk = tokens[0]
            if (tk == rt.id.value):
                game_records.append(game_record())
                game_itr = game_records[-1]
                game_itr.id = tokens[1]
            elif game_itr is not None:
                game_itr.add(tokens)

    for game in game_records:
        for starter in game.starters:
            if (starter.start_field_pos == fpos.C):
                print (starter.name,fpos.getname(starter.start_field_pos))
        #for sub in game.substitutions:
        #    if (sub)

    return

if __name__=="__main__":
    main()