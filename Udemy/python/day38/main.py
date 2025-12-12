from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_NINJAS_KEY = os.getenv("API_NINJAS_KEY")
SHEETY_API_KEY = os.getenv("SHEETY_API_KEY")

def fetch_workout_calories(activity: str, duration: int, weight: int) -> int:
    print("Fetching workout calories...")
    url = "https://api.api-ninjas.com/v1/caloriesburned"
    headers = {"X-Api-Key": API_NINJAS_KEY}
    params = {"activity": activity, "duration": duration, "weight": weight}
    response = requests.get(url, headers=headers, params=params)
    
    response.raise_for_status()

    data = response.json()
    return data[0]["total_calories"]


def post_workout_summary(activity: str, duration: int, calories: int, date: str, time: str):
    print("Posting workout summary...")
    print(f"Activity: {activity}, Duration: {duration} mins, Calories: {calories}, Date: {date}, Time: {time}")
    url = "https://api.sheety.co/ac3343d7e43253f7bd26f2f521181aa4/myWorkouts/workouts"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {SHEETY_API_KEY}"}
    workout_data = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": activity,
            "duration": duration,
            "calories": calories
        }
    }
    response = requests.post(url, json=workout_data, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    activity = input("Enter the type of workout (e.g., running, cycling): ")
    duration = int(input("Enter the duration of the workout in minutes: "))
    weight = int(input("Enter your weight in pounds: "))

    calories= fetch_workout_calories(activity, duration, weight)
    post_workout_summary(activity.capitalize(),
                         duration,
                         calories,
                         datetime.now().strftime("%d/%m/%Y"),
                         datetime.now().strftime("%H:%M:%S"))
    

if __name__ == "__main__":
    main()
