
import mlbgame
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import myql
from myql.utils import pretty_json, pretty_xml

import json
import webbrowser
import time
from rauth import OAuth1Service
from rauth.utils import parse_utf8_qsl

'''
https://vicmora.github.io/blog/2017/03/17/yahoo-fantasy-sports-api-authentication
'''

credentials_file = open('oauth.json')
credentials = json.load(credentials_file)
credentials_file.close()

oauth = OAuth1Service(consumer_key = credentials['consumer_key'],
                      consumer_secret = credentials['consumer_secret'],
                      name = "yahoo",
                      request_token_url = "https://api.login.yahoo.com/oauth/v2/get_request_token",
                      access_token_url = "https://api.login.yahoo.com/oauth/v2/get_token",
                      authorize_url = "https://api.login.yahoo.com/oauth/v2/request_auth",
                      base_url = "http://fantasysports.yahooapis.com/")

request_token, request_token_secret = oauth.get_request_token(params={"oauth_callback": "oob"})

authorize_url = oauth.get_authorize_url(request_token)
webbrowser.open(authorize_url)
verify = raw_input('Enter code: ')

raw_access = oauth.get_raw_access_token(request_token,
                                        request_token_secret,
                                        params={"oauth_verifier": verify})

parsed_access_token = parse_utf8_qsl(raw_access.content)
access_token = (parsed_access_token['oauth_token'], parsed_access_token['oauth_token_secret'])

start_time = time.time()
end_time = start_time + 3600

credentials['access_token'] = parsed_access_token['oauth_token']
credentials['access_token_secret'] = parsed_access_token['oauth_token_secret']
tokens = (credentials['access_token'], credentials['access_token_secret'])

s = oauth.get_session(tokens)

url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431/teams'
r = s.get(url, params={'format': 'json'})
#r = s.get('http://fantasysports.yahooapis.com/fantasy/v2/game/nfl', )
r.status_code
r.json()

#yql = myql.MYQL(format='xml', community=True)
##response = yql.raw_query("select * from fantasysports.games where game_key='nfl'")
#response = yql.get('api-secure.sports.yahoo.com', 'game_key', 1)
#print(pretty_xml(response.content))


game_id = '361102105'
game_url = 'https://query.yahooapis.com/v1/public/yql?'
#game_url = 'http://fantasysports.yahooapis.com/fantasy/v2/game/mlb' #+ game_id
#game_url = 'https://api-secure.sports.yahoo.com/v1/editorial/s/boxscore/mlb.g.' + game_id #

#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
response = requests.get(game_url) #, headers=headers)
game_data = response.json()

day = mlbgame.day(2018, 4, 16, home='Padres', away='Dodgers')
#games = mlbgame.combine_games(month)
#for game in games:
#    print(game)

game = None
events = None
if (day != None):
    if len(day) > 0:
        game = day[0]
        print('[{}] {}'.format(game.game_id, game))
        events = mlbgame.game_events(game.game_id)
        for evt in events:
            evt.nice_output()
            for t in evt.top:
                pitches = t.pitches
                #for p in pitches:
                #    print (p.sv_id)

        #players = mlbgame.players(game.game_id)
#        for p in players.home_players:
#            print('{}, {}'.format(p.last, p.first))

#        for p in players.away_players:
#            print('{}, {}'.format(p.last, p.first))



game_id = '361102105'
#game_url = 'http://fantasysports.yahooapis.com/fantasy/v2/game/pmlb/' + game_id
game_url = 'https://api-secure.sports.yahoo.com/v1/editorial/s/boxscore/mlb' # + game_id + \
#            '?lang=en-US&region=US&tz=America%2FChicago&ysp_redesign=1&mode=&v=4&ysp_enable_last_update=1&polling=1'

#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
response = requests.get(game_url) #, headers=headers)
game_data = response.json()

pitches = game_data['service']['boxscore']['gamepitches']['mlb.g.' + game_id]

print("Total number of pitches thrown during the game: " + str(len(pitches)))

pitch_df = pd.DataFrame(pitches)
pitch_df.head()

transpose_pitch_df = pitch_df.transpose()
transpose_pitch_df.head()

for val in list(transpose_pitch_df.columns.values):
    transpose_pitch_df[val] = transpose_pitch_df[val].convert_objects(convert_numeric=True)

transpose_pitch_df.dtypes

pitcher_list = transpose_pitch_df.pitcher.unique()
for pitcher in pitcher_list:
    pitcher_url = 'http://sports.yahoo.com/mlb/players/' + str(pitcher) + '/'
    req = requests.get(pitcher_url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    pitcher_info = soup.title.string
    print(pitcher_info.split('|')[0] + " of the " + pitcher_info.split('|')[1] + "(Yahoo ID: " + str(pitcher) + ")")

kluber = transpose_pitch_df[transpose_pitch_df.pitcher == 9048]
hendricks = transpose_pitch_df[transpose_pitch_df.pitcher == 9758]

#plt.figure(figsize=(6,6))
#plt.subplot(111)
#k_max = kluber.velocity.max()
#k_min = kluber.velocity.min()
#ax1 = kluber['velocity'].hist(bins=int(k_max - k_min))
#plt.xlim(70, 100)
#plt.title('Corey Kluber Pitch Velocity - Game 7')
#plt.xlabel('Pitch Velocity')
#plt.ylabel('Number of Pitches')
#plt.show()

#plt.figure(figsize=(6,6))
#plt.subplot(111)
#h_max = hendricks.velocity.max()
#h_min = hendricks.velocity.min()
#ax2 = hendricks['velocity'].hist(bins=int(h_max - h_min))
#plt.xlim(70, 100)
#plt.title('Kyle Hendricks Pitch Velocity - Game 7')
#plt.xlabel('Pitch Velocity')
#plt.ylabel('Number of Pitches')
#plt.show()

sorted_kluber_pitches = kluber.sort_values(['play_num'])
sorted_hendricks_pitches = hendricks.sort_values(['play_num'])
kluber_balls = sorted_kluber_pitches[sorted_kluber_pitches.result == 0]
hendricks_balls = sorted_hendricks_pitches[sorted_hendricks_pitches.result == 0]
kluber_others = sorted_kluber_pitches[sorted_kluber_pitches.result != 0]
hendricks_others = sorted_hendricks_pitches[sorted_hendricks_pitches.result != 0]

plt.figure(figsize=(6,6))
ax = plt.subplot(111)
ax.scatter(transpose_pitch_df[transpose_pitch_df.result == 0].horizontal,
                    transpose_pitch_df[transpose_pitch_df.result == 0].vertical,
                    marker='o', label='balls')

ax.set_xlim(-20000,20000)
ax.set_ylim(-20000,20000)

#Axis labels
ax.set_xlabel('Horizontal')
ax.set_ylabel('Vertical')

#set title
ax.set_title('The Strike Zone',
             y=1.0, fontsize=18)

#show legend
ax.legend(loc=3, frameon=True, shadow=True)
plt.show()

# create our jointplot
joint_chart = sns.jointplot(hendricks_others.horizontal,
                                 hendricks_others.vertical,
                                 stat_func=None,
                                 color='r',
                                 marker='o',
                                 s=50,
                                 kind='scatter',
                                 space=0,
                                 label='Strikes/Hits/Fouls',
                                 alpha=1.0)

joint_chart.fig.set_size_inches(6,6)

joint_chart.x = hendricks_balls.horizontal
joint_chart.y = hendricks_balls.vertical
joint_chart.plot_joint(plt.scatter, marker='o',
                       c='b', s=50,label='Balls')

ax = joint_chart.ax_joint

ax.set_xlim(-20000,20000)
ax.set_ylim(-20000, 20000)

# Get rid of axis labels and tick marks
#ax.set_xlabel('')
#ax.set_ylabel('')
#ax.tick_params(labelbottom='off', labelleft='off')

# Add a title and legend
ax.set_title('Kyle Hendricks: Stikes/Fouls/Balls Hit',
             y=1.2, fontsize=18)
ax.legend(loc=3, frameon=True, shadow=True)

# Add Data Scource and Author
#ax.text(-20000,-20000,'Data Source: Yahoo!'
#        '\nAuthor: Gregory Brunner, @gregbrunn',
#        fontsize=12)
plt.show()

joint_chart = sns.jointplot(kluber_others.horizontal,
                                 kluber_others.vertical,
                                 stat_func=None,
                                 color='r',
                                 marker='o',
                                 s=50,
                                 kind='scatter',
                                 space=0,
                                 label='Strikes/Hits/Fouls',
                                 alpha=1.0)

joint_chart.fig.set_size_inches(6,6)

joint_chart.x = kluber_balls.horizontal
joint_chart.y = kluber_balls.vertical
joint_chart.plot_joint(plt.scatter, marker='o',
                       c='b', s=50,label='Balls')

ax = joint_chart.ax_joint

ax.set_xlim(-20000,20000)
ax.set_ylim(-20000, 20000)

# Get rid of axis labels and tick marks
#ax.set_xlabel('')
#ax.set_ylabel('')
#ax.tick_params(labelbottom='off', labelleft='off')

# Add a title and legend
ax.set_title('Corey Kluber: World Series Game 7',
             y=1.2, fontsize=18)
ax.legend(loc=3, frameon=True, shadow=True)


# Add Data Scource and Author
#ax.text(-20000,-20000,'Data Source: Yahoo!'
#        '\nAuthor: Gregory Brunner, @gregbrunn',
#        fontsize=12)
plt.show()

play_by_play = game_data['service']['boxscore']['gameplay_by_play']['mlb.g.' + game_id]
play_by_play_df = pd.DataFrame(play_by_play)
play_by_play_df.transpose().head()

