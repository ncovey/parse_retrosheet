
import pybaseball

#data = pybaseball.statcast(start_dt='2018-04-17', end_dt='2018-04-17')
#print(data.head(200000))

p = pybaseball.playerid_lookup('jansen', 'kenley')
pid = int(p.key_mlbam)

jansen_stats = pybaseball.statcast_pitcher('2017-04-01', '2017-4-30', pid)
print(jansen_stats.head(200))

data = pybaseball.pitching_stats(2012, 2016)
data.head()

data = pybaseball.batting_stats_range('2017-05-01', '2017-05-08')
data.head()

data = pybaseball.schedule_and_record(1927, 'NYY')
data.head()