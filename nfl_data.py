import pandas as pd
import numpy as np
import scipy.stats as stats

# import beautifulsoup4 as bs4
import requests
from lxml import etree

np.set_printoptions(linewidth = 400)
pd.set_option('line_width', 400)
pd.set_option('max_rows', None)
pd.set_option('max_columns', None)



import config
print config.truck['color']


def get_schedule():
    BASE_URL = "http://api.fantasyfootballnerd.com"
    football_url = BASE_URL + "/ffnScheduleXML.php?apiKey=" + FFN_KEY
    # r = requests.get(football_url)
    # print r.content
    doc = etree.parse(football_url)
    df_list = []
    for i in doc.iter():
        try:
            a = pd.DataFrame(i.values())
            print a
            df_list.append(a.T)
        except:
            print "pass"
    df = pd.concat(df_list, ignore_index = 1).rename(columns = {1: 'week', 2: 'date', 3: 'away', 4: 'home', 5: 'time'})
    df = df.drop([0], axis = 1).dropna(axis = 0, how='any')
    return df


def get_player_stats(week):
    BASE_URL = "http://api.fantasyfootballnerd.com"
    postions = ['QB', 'RB', 'WR', 'TE', 'DEF', 'K']
    df_all_postions = []
    for i in postions:
        football_url = BASE_URL + "/ffnSitStartXML.php?apiKey=" + FFN_KEY + "&week=%s&position=%s" %(str(week), i)
        doc = etree.parse(football_url)
        df_list = []
        for i in doc.iter():
            try:
                a = pd.DataFrame(i.values())
                df_list.append(a.T)
            except:
                print "pass"
        df = pd.concat(df_list, ignore_index = 1).rename(columns = {1: 'name', 2: 'position', 3: 'team', 4: 'week', 5: 'rank', 6:'proj_pts'})
        df = df.drop([0], axis = 1).dropna(axis = 0, how='any')
        df = df[:15]
        df_all_postions.append(df)
    all_postions = pd.concat(df_all_postions, ignore_index = True)
    return all_postions

##
# schedule = get_schedule()

# all_player_rank = get_player_stats(5)


def pull_yahoo_data():
    # import urllib2
    # result = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20title%2Cabstract%20from%20search.web%20where%20query%3D%22paul%20tarjan%22&format=json").read()
    # import simplejson
    # data = simplejson.loads(result)
    # data['query']['results']['result'][0]['title']



def using_nfl_game_old(year, weeknum):
    games = nflgame.games(year, week=weeknum)
    players = nflgame.combine_game_stats(games)
    # player_list = []
    player_list_p = []
    player_list_r = []
    player_list_wr = []
    player_dict_rush = {}
    player_dict_pass = {}
    player_dict_receive = {}

    for p in players.rushing():
        player_dict_rush = {
            'player': '%s' %p,
            'playerid': p.playerid,
            'rushing_att' + str(weeknum): p.rushing_att,
            'rushing_yds' + str(weeknum): p.rushing_yds,
            'rushing_tds' + str(weeknum): p.rushing_tds
        }
        player_list_r.append(player_dict_rush)

    for p in players.passing():
        player_dict_pass = {
            'player': '%s' %p,
            'playerid': p.playerid,
            'passing_att' + str(weeknum): p.passing_att,
            'passing_yds' + str(weeknum): p.passing_yds,
            'passing_tds' + str(weeknum): p.passing_tds
        }
        player_list_p.append(player_dict_pass)

    for p in players.receiving():
        player_dict_receive = {
            'player': '%s' %p,
            'playerid': p.playerid,
            'receiving_tar' + str(weeknum): p.receiving_tar,
            'receiving_rec' + str(weeknum): p.receiving_rec,
            'receiving_yds' + str(weeknum): p.receiving_yds,
            'receiving_tds' + str(weeknum): p.receiving_tds
        }
        player_list_wr.append(player_dict_receive)
    # df_pass = pd.DataFrame(player_dict_pass)
    df_rush = pd.DataFrame(player_list_r)
    df_pass = pd.DataFrame(player_list_p)
    df_receive = pd.DataFrame(player_list_wr)

    df = pd.merge(df_rush, df_pass, on=["playerid", "player"], how="outer")
    df2 = pd.merge(df, df_receive, on=["playerid", "player"], how="outer")
    # return df_rush, df_pass, df_receive
    return df2

import nflgame
def using_nfl_game(year, weeknum):
    games = nflgame.games(year, week=weeknum)
    # players = nflgame.combine_game_stats(games)
    players = nflgame.combine_play_stats(games)
    player_list = []
    player_dict = {}

    for p in players:
        # print p.formatted_stats()
        player_dict = {
            'player': '%s' %p,
            'player_pos': str(p.player),
            'playerid': p.playerid,
            'team': p.team,
            'rushing_att' + str(weeknum): p.rushing_att,
            'rushing_yds' + str(weeknum): p.rushing_yds,
            'rushing_tds' + str(weeknum): p.rushing_tds,
            'passing_att' + str(weeknum): p.passing_att,
            'passing_cmp' + str(weeknum): p.passing_cmp,
            'passing_cmp_air_yds' + str(weeknum): p.passing_cmp_air_yds,
            'passing_incmp' + str(weeknum): p.passing_incmp,
            'passing_incmp_air_yds' + str(weeknum): p.passing_incmp_air_yds,
            'passing_int' + str(weeknum): p.passing_int,
            'passing_sk' + str(weeknum): p.passing_sk,
            'passing_sk_yds' + str(weeknum): p.passing_sk_yds,
            'passing_yds' + str(weeknum): p.passing_yds,
            'passing_tds' + str(weeknum): p.passing_tds,
            'receiving_tar' + str(weeknum): p.receiving_tar,
            'receiving_rec' + str(weeknum): p.receiving_rec,
            'receiving_yds' + str(weeknum): p.receiving_yds,
            'receiving_tds' + str(weeknum): p.receiving_tds,
            'receiving_yac_yds' + str(weeknum): p.receiving_yac_yds
            # 'formatted_stats' + str(weeknum): p.formatted_stats()
        }
        player_list.append(player_dict)

    df_players = pd.DataFrame(player_list)

    return df_players

def work_with_nflgame(startweek = 1, endweek = 1):
    # using_nfl_game(2013, 7)
    # off_df_list = []
    for week in range(startweek, endweek + 1):
        print week, " ",
        df = using_nfl_game(2013, week)
        if week == 1:
            df['QB'] = df.player_pos.apply(lambda x: True if x.find('(QB') >= 1 else False)
            df['WR'] = df.player_pos.apply(lambda x: True if x.find('(WR') >= 1 else False)
            df['RB'] = df.player_pos.apply(lambda x: True if x.find('(RB') >= 1 else False)
            df['FB'] = df.player_pos.apply(lambda x: True if x.find('(FB') >= 1 else False)
            df_all = pd.DataFrame(df)
        else:
            df_all = pd.merge(df_all, df.drop(['player', 'player_pos', 'team'], axis=1), on=['playerid'], how='outer')

    df_all['_offence'] = pd.DataFrame(df_all, columns = ['QB', 'WR', 'RB', 'FB']).apply(lambda x: x.max(), axis=1)

    df_offence = df_all[df_all['_offence'] == True]

    df_defence = df_all[df_all['_offence'] == False]

    # sum up the different vars
    passing_vars = ['passing_att', 'passing_cmp', 'passing_cmp_air_yds', 'passing_incmp', 'passing_incmp_air_yds', 'passing_int', \
        'passing_sk', 'passing_sk_yds', 'passing_yds', 'passing_tds']
    rush_vars = ['rushing_att', 'rushing_yds', 'rushing_tds']
    receive_vars = ['receiving_tar', 'receiving_rec', 'receiving_yds', 'receiving_tds', 'receiving_yac_yds']

    for _var in passing_vars + rush_vars + receive_vars:
        df_offence[_var + '_sum'] = df_offence[[_var + str(i) for i in range(startweek, endweek + 1)]].sum(axis = 1)

    # get number of weeks active
    # df_offence[['rushing_att' + str(i) for i in range(startweek, endweek + 1)]].replace(0, np.nan, inplace=True)
    df_offence['rushing_count'] = df_offence[['rushing_att' + str(i) for i in range(startweek, endweek + 1)]].apply(lambda x: x.count(), axis=1)


    # count_list = ['rushing_att' + str(i) for i in range(startweek, endweek + 1)]


def nfldb(year = 2013):
    import nfldb
    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=year, season_type='Regular')
    for pp in q.sort('passing_yds').limit(15).as_aggregate():
        print pp.player, pp.passing_yds, pp.rushing_tds

    print "\n"

    for pp in q.sort('rushing_yds').limit(15).as_aggregate():
        print pp.player, pp.rushing_yds, pp.rushing_tds

    # SELECT player.full_name, SUM(play_player.passing_yds) AS passing_yds
    # FROM play_player
    # LEFT JOIN player ON player.player_id = play_player.player_id
    # LEFT JOIN game ON game.gsis_id = play_player.gsis_id
    # WHERE game.season_year = 2012 AND game.season_type = 'Regular'
    # GROUP BY player.full_name
    # HAVING SUM(play_player.passing_yds) >= 4500
    # ORDER BY passing_yds DESC

