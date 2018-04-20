
import mlbgame
import pybaseball

from multiprocessing import Pool

class Battery():
    def __init__():
        self.pitcher = None
        self.catcher = None


#def getpitchers(year):
    
#    batteries = []

#    mlbgame.combine_games(year)



def main():

    pool = Pool()
    res = []
    years = []
    #for y in range(2008, 2009): # 2018
    #    res.append(pool.apply_async(mlbgame.games, [y]))

    #for n in res:
    #    years.append(n.get(timeout=120))
    
    years = [mlbgame.games(2008, 4, 18)]

    batteries = []
    for y in years:
        games = mlbgame.combine_games(y)
        for game in games:
            events = mlbgame.game_events(game.game_id)
            stats = mlbgame.player_stats(game.game_id)
            players = mlbgame.players(game.game_id)
            overview = mlbgame.overview(game.game_id)
            print (game.home_team)
            for player in players.home_players:
                if player.position == 'P':
                    print (player.last, player.first, player.position)
                elif player.position == 'C':
                    print (player.last, player.first, player.position)
            print (game.away_team)
            for player in players.away_players:
                if player.position == 'P':
                    print (player.last, player.first, player.position)
                elif player.position == 'C':
                    print (player.last, player.first, player.position)
            #print(e for e in events)
            #print(s for s in stats)
            #print(p for p in players)
            #for e in events:
            #    for t in e.top:
            #        print(t.event, t.pitcher)
                #for t in e.bottom:
                #    print(t.event, t.pitcher)

    #day = mlbgame.day(2018, 4, 16, home='Padres', away='Dodgers')
    ##games = mlbgame.combine_games(month)
    ##for game in games:
    ##    print(game)

    #game = None
    #events = None
    #if (day != None):
    #    if len(day) > 0:
    #        game = day[0]
    #        print('[{}] {}'.format(game.game_id, game))
    #        events = mlbgame.game_events(game.game_id)
    #        for evt in events:
    #            evt.nice_output()
    #            for t in evt.top:
    #                pitches = t.pitches
    #                #for p in pitches:
    #                #    print (p.sv_id)

    #        #players = mlbgame.players(game.game_id)
    ##        for p in players.home_players:
    ##            print('{}, {}'.format(p.last, p.first))

    ##        for p in players.away_players:
    ##            print('{}, {}'.format(p.last, p.first))

if __name__ == "__main__":
    #freeze_support()
    main()
