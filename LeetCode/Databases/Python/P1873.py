# https://leetcode.com/problems/calculate-special-bonus/

import numpy as np
import pandas as pd

def calculate_special_bonus(employees: pd.DataFrame) -> pd.DataFrame:
    #Solution #1
    #employees['bonus'] = employees.apply(
    #    lambda x: x['salary'] if x['employee_id']%2 == 1 and not x['name'].startswith('M') else 0,
    #    axis = 1 # apply along rows
    #)
    
    #Solution #2
    #employees.loc[(employees['employee_id'] %2 == 1) & (employees['name'][0] != 'M'), 'bouns'] = employees['salary']

    employees['bonus'] = np.where(
        (employees['employee_id'] %2 == 1) & (~employees['name'].str.startswith('M')),
        employees['salary'], 0)
    return employees[['employee_id', 'bonus']].sort_values('employee_id')