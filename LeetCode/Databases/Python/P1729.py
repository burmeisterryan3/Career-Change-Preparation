# https://leetcode.com/problems/find-followers-count/

import pandas as pd

def count_followers(followers: pd.DataFrame) -> pd.DataFrame:
    return followers.groupby(['user_id'])\
        .count()\
        .sort_values(by='user_id')\
        .reset_index()\
        .rename(columns={'follower_id': 'followers_count'})