import helpers
import json
import pandas as pd

def get_season_schedule(season: int):

    url = f'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{season}/league/00_full_schedule.json'
    json_set = helpers.request_json(url)

    all_df = pd.DataFrame()
    for d in json_set['lscd']: 
        df = pd.DataFrame(d['mscd']['g'])    
        all_df = pd.concat([all_df, df])

    all_df = pd.concat([all_df.drop(['h'], axis=1), all_df.h.apply(pd.Series).add_prefix('homeTeam_')], axis=1)
    all_df = pd.concat([all_df.drop(['v'], axis=1), all_df.v.apply(pd.Series).add_prefix('awayTeam_')], axis=1)
    
    drop_list = ['bd', 'seri', 'is', 'st', 'stt', 'gdtutc', 'utctm', 'ppdst', 'homeTeam_s', 'awayTeam_s', 
             'awayTeam_tc', 'homeTeam_tc', 'homeTeam_re', 'awayTeam_re', 'awayTeam_tn', 'homeTeam_tn']

    all_df = all_df.drop(drop_list, axis=1)
    
    columns_dict = {
        'gid': 'GAME_ID',
        'gcode': 'GAME_CODE',
        'seq': 'GAME_DATE_SEQ',
        'gdte': 'GAME_DATE_ET',
        'htm': 'HOME_TIME',
        'vtm': 'AWAY_TIME',
        'etm': 'GAME_TIME_ET',
        'an': 'ARENA',
        'ac': 'CITY',
        'as': 'STATE',
        'homeTeam_tid': 'HOME_TEAM_ID',
        'homeTeam_ta': 'HOME_TEAM_CD',
        'awayTeam_tid': 'HOME_TEAM_ID',
        'awayTeam_ta': 'AWAY_TEAM_CD'
    }
    
    all_df.rename(columns=columns_dict, inplace=True)
    all_df = all_df.sort_values(['GAME_DATE_ET', 'GAME_DATE_SEQ'])
        
    return all_df

def get_game_boxscore(game_id: str):

    url = f'https://stats.nba.com/stats/boxscoretraditionalv3?GameID={game_id}&LeagueID=00&endPeriod=0&endRange=28800&rangeType=0&startPeriod=0&startRange=0'
    json_set = helpers.request_json(url)

    data = json_set['boxScoreTraditional']
    game_id = data['gameId']
    home_team_id = data['homeTeamId']
    away_team_id = data['awayTeamId']

    df_home = pd.DataFrame(data['homeTeam']['players'])
    df_home = pd.concat([df_home.drop(['statistics'], axis=1), df_home.statistics.apply(pd.Series)], axis=1)
    df_home['team_id'] = home_team_id
    df_home['team_type'] = 'HOME'

    df_away = pd.DataFrame(data['awayTeam']['players'])
    df_away = pd.concat([df_away.drop(['statistics'], axis=1), df_away.statistics.apply(pd.Series)], axis=1)
    df_away['team_id'] = away_team_id
    df_away['team_type'] = 'AWAY'

    df_game = pd.concat([df_home, df_away], sort=False)
    df_game['game_id'] = game_id

    drop_list = ['nameI', 'playerSlug', 'comment', 'jerseyNum']
    df_game = df_game.drop(drop_list, axis=1)

    columns_dict = {
        'personId':'PLAYER_ID',
        'firstName':'FIRST_NAME',
        'familyName':'LAST_NAME',
        'position':'POS',
        'minutes':'MIN',
        'fieldGoalsMade':'FGM',
        'fieldGoalsAttempted':'FGA',
        'fieldGoalsPercentage':'FG%',
        'threePointersMade':'3PM',
        'threePointersAttempted':'3PA',
        'threePointersPercentage':'3P%',
        'freeThrowsMade':'FTM',
        'freeThrowsAttempted':'FTA',
        'freeThrowsPercentage':'FT%',
        'reboundsOffensive':'ORB',
        'reboundsDefensive':'DRB',
        'reboundsTotal':'REB',
        'assists':'AST',
        'steals':'STL',
        'blocks':'BLK',
        'turnovers':'TOV',
        'foulsPersonal':'PF',
        'points':'PTS',
        'plusMinusPoints':'PLUS_MINUS',
        'team_id':'TEAM_ID',
        'team_type':'TEAM_TYPE',
        'game_id':'GAME_ID'
    }
    df_game.rename(columns=columns_dict, inplace=True)

    reorder_list = [
        'GAME_ID', 'TEAM_ID', 'TEAM_TYPE', 'PLAYER_ID', 'FIRST_NAME', 'LAST_NAME', 'POS', 'MIN', 'FGM', 'FGA',
        'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'ORB', 'DRB', 'REB',
        'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 
    ]
    df_game = df_game[reorder_list]

    return df_game