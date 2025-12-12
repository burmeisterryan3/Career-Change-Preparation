import datetime as dt
import os

from dotenv import load_dotenv

load_dotenv()

now = dt.datetime.now()
print(f"now: {now}")
print(f"year: {now.year}")
print(f"type: {type(now.year)}")
print(f"day (0 - Monday): {now.weekday()}")
print(f"day: {dt.datetime.today().strftime('%A')}")

birth_year = int(os.getenv("BIRTH_YEAR"))
birth_month = int(os.getenv("BIRTH_MONTH"))
birth_day = int(os.getenv("BIRTH_DAY"))

birthday = dt.datetime(year=birth_year, month=birth_month, day=birth_day)
print(f"birthday: {birthday}")
