"""Day 35."""

import os

import requests
from dotenv import load_dotenv
from twilio.rest import Client

LAT = "36.850769"
LON = "-76.285873"

TEST_LAT = "33.543682"
TEST_LON = "-86.779633"


def check_for_umbrella(wx_data: dict) -> bool:
    bring_umbrella = False
    for fcast in wx_data["list"]:
        condition_code = fcast["weather"][0]["id"]
        if condition_code < 700:
            bring_umbrella = True
            break

    return bring_umbrella


def get_twilio_client() -> Client:
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    return Client(account_sid, auth_token)


if __name__ == "__main__":
    load_dotenv()

    parameters = {
        # "lat": LAT,
        # "lon": LON,
        "lat": TEST_LAT,
        "lon": TEST_LON,
        "cnt": 4,
        "appid": os.getenv("APP_ID"),
    }

    resp = requests.get(
        url="https://api.openweathermap.org/data/2.5/forecast",
        params=parameters,
    )
    resp.raise_for_status()

    wx_data = resp.json()
    bring_umbrella = check_for_umbrella(wx_data)

    if bring_umbrella:
        client = get_twilio_client()
        message = client.messages.create(
            body="Bring an umbrella!",
            from_=os.getenv("TWILIO_MY_NUMBER"),
            to=os.getenv("TWILIO_VIRTUAL_NUMBER"),
        )

        print(f"message status: {message.status}")
