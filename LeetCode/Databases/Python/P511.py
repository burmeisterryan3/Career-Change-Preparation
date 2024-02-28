# https://leetcode.com/problems/game-play-analysis-i/

import pandas as pd

def game_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    return activity[['player_id', 'event_date']]\
        .groupby(['player_id'])\
        .min()\
        .rename(columns={'event_date': 'first_login'})\
        .reset_index()