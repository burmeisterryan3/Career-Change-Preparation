# https://leetcode.com/problems/actors-and-directors-who-cooperated-at-least-three-times/

import pandas as pd

def actors_and_directors(actor_director: pd.DataFrame) -> pd.DataFrame:
    # return actor_director[actor_director\
    # .groupby(['actor_id', 'director_id'])\
    #    .transform('size') >= 3][['actor_id', 'director_id']].drop_duplicates()
    df = actor_director[['actor_id', 'director_id']].value_counts().reset_index()
    return df[df['count'] >= 3][['actor_id', 'director_id']]