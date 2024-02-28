# https://leetcode.com/problems/duplicate-emails/

import pandas as pd

def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    # return person[person.duplicated(subset='email')][['email']].drop_duplicates()
    return person[['email']].value_counts().loc[lambda x: x > 1].reset_index()[['email']]