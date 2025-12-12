"""Day 36. API Development - Stock SMS messaging."""

import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_TOKEN = os.getenv("ALPHA_AUTH_TOKEN")
NEWS_TOKEN = os.getenv("NEWS_AUTH_TOKEN")
NUM_ARTICLES = 1  # Restrictions on message size due to Twilio trial account


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stock_daily(symbol: str):
    """Get a daily set of values for a particular stock via the Alpha Vantage API."""
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_TOKEN,
    }
    resp = requests.get(
        url="https://www.alphavantage.co/query", params=parameters
    )
    resp.raise_for_status()

    return resp.json()


def get_prior_day_close(values: dict, dt: datetime):
    """Get the closing value for a stock the last day the market was open."""
    prior_day = dt
    while True:
        prior_day -= timedelta(days=1)
        try:
            close = values["Time Series (Daily)"][
                prior_day.strftime("%Y-%m-%d")
            ]["4. close"]

            return (float(close), prior_day)
        except KeyError:
            continue


def get_change(end: float, start: float):
    """Get the percent change between the stock value at two dates."""
    difference = end - start
    perc_change = (difference / float(end)) * 100
    return (difference, perc_change)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def get_news(company: str, start_date: str, end_date: str) -> dict:
    """Get news articles via the News API."""
    headers = {"Authorization": f"{NEWS_TOKEN}"}
    parameters = {
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d"),
        "language": "en",
        "sortBy": "relevancy",
        "q": company,
    }
    resp = requests.get(
        "https://newsapi.org/v2/everything",
        headers=headers,
        params=parameters,
    )
    resp.raise_for_status()
    return resp.json()["articles"][:NUM_ARTICLES]


def generate_message(ticker: str, perc_change: float, articles: dict) -> str:
    """Generate a message detailing news about the stock. Shortened due to Twilio trial requirements."""
    message = ticker + ": "

    if perc_change < 0:
        message += f"🔻{int(abs(perc_change))}%"
    elif perc_change > 0:
        message += f"🔺{int(abs(perc_change))}%"
    else:
        message += "-"

    message += "\n"
    for article in articles:
        message += "\n"
        message += f"Headline: {article['title']}\n"
        # Restrictions on message size due to Twilio trial account
        # message += f"Brief: {article['description']}\n"

    return message


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
def get_twilio_client() -> Client:
    """Get a Twilio client to send SMS messages."""
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    return Client(account_sid, auth_token)


def send_message(message: str):
    """Send an SMS message with the stock info via Twilio."""
    client = get_twilio_client()
    message = client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_MY_NUMBER"),
        to=os.getenv("TWILIO_VIRTUAL_NUMBER"),
    )

    print(f"message status: {message.status}")


if __name__ == "__main__":
    values = get_stock_daily(STOCK)

    last_close, last_date = get_prior_day_close(values, datetime.today())
    sec_to_last_close, day_b4_last = get_prior_day_close(values, last_date)

    abs_change, perc_change = get_change(last_close, sec_to_last_close)

    articles = get_news(COMPANY_NAME, day_b4_last, last_date)
    message = generate_message(STOCK, perc_change, articles)
    send_message(message)
