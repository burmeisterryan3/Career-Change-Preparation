import json
import os

import tweepy
from dotenv import load_dotenv


def scrape_user_tweets(
    username: str, n_tweets: int = 5, mock: bool = True
) -> list[dict[str, str]]:
    """Scrapes a user's tweets from X."""
    tweet_list = []

    mock = True
    if mock:
        with open(
            "third_parties/__cache__/tweets.json", encoding="utf-8"
        ) as f:
            tweets = json.load(f)
    else:
        # Code as example... don't have the API tokens
        twitter_client = tweepy.Client(
            bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
            consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
            consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
            access_token=os.environ["TWITTER_ACCESS_TOKEN"],
            access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        )

        user_id = twitter_client.get_user(username).data.id
        tweets = twitter_client.get_users_tweets(
            user_id, max_results=n_tweets, exclude=["retweets", "replies"]
        )

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://x.com/{username}/status/{tweet['id']}"
        tweet_list.append(tweet_dict)

    return tweets


if __name__ == "__main__":
    load_dotenv()

    tweets = scrape_user_tweets(username="EdenEmarco177")
    print(tweets)
