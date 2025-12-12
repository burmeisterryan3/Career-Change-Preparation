import requests
from dotenv import load_dotenv
from collections import namedtuple
import os

load_dotenv()
URL = os.getenv("SHEETY_URL")
SHEETY_API_KEY = os.getenv("SHEETY_API_KEY")


class DataManager:
    def __init__(self):
        pass
    
    def get_data(self):
        headers = {"Authorization": f"Bearer {SHEETY_API_KEY}"}
        response = requests.get(url=self.URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        

