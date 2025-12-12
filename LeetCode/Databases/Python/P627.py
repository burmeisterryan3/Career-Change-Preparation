# https://leetcode.com/problems/swap-salary/

import pandas as pd

def swap_genders(x):
    return 'm' if x == 'f' else 'f'

def swap_salary(salary: pd.DataFrame) -> pd.DataFrame:
    # salary['sex'] = salary['sex'].map(lambda x: 'm' if x == 'f' else 'f')
    # salary['sex'] = salary['sex'].map(swap_genders)
    # salary['sex'] = salary['sex'].map({'m': 'f', 'f': 'm'})
    # salary['sex'] = salary['sex'].replace({'m': 'f', 'f': 'm'})
    salary['sex'] = salary['sex'].apply(swap_genders)
    return salary