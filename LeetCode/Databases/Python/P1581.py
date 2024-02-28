# https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/

import pandas as pd

def solution_groupby_size(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['transaction_id'].isna()]\
        .groupby('customer_id')\
        .size()\
        .reset_index(name='count_no_trans')

def solution_groupby_count(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['transaction_id'].isna()]\
        .groupby('customer_id', as_index=False)['visit_id']\
        .count()\
        .rename(columns={'visit_id': 'count_no_trans'})

def find_customers(visits: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    # option 1 - pd.Sereis.isin()
    # return solution_groupby_count(visits[~visits['visit_id'].isin(transactions['visit_id'])])

    # option 2 - pd.DataFrame.merge
    # joined_df = visits.merge(transactions, on='visit_id', how='left')
    
    # option 3 - pd.DataFrame.join
    joined_df = visits.join(transactions.set_index('visit_id'), on='visit_id')
    
    # return solution_goupby_size(joined_df)
    return solution_groupby_count(joined_df)