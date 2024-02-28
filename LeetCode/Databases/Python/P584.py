# https://leetcode.com/problems/find-customer-referee/

import pandas as pd

def find_customer_referee(customer: pd.DataFrame) -> pd.DataFrame:
    df = customer[(customer['referee_id'] != 2) | (customer['referee_id'].isnull())]
    return df[['name']]