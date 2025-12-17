from datetime import datetime
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import spotipy  # type: ignore
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
URL = "https://www.billboard.com/charts/hot-100/"
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_USER_ID = os.getenv("SPOTIFY_USER_ID")
PLAYLIST_ID = "Udemy-Top-100"
# REDIRECT_URI = "https://open.spotify.com/"
REDIRECT_URI = "https://127.0.0.1:8080/callback"


def get_date():
    """Get a date to search against the Billboard Top 100."""
    user_input = input(
        "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
    )
    try:
        datetime.strptime(user_input, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid input provided.")

    return user_input


def get_web_page() -> str:
    """Get the Billboard Topp 100 html response object."""
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
    }

    return requests.get(URL, headers=header).text


def get_top_100(html: str) -> list[str]:
    """Parse html to find top 100 songs."""
    soup = BeautifulSoup(html, "html.parser")
    songs = [
        song.getText().strip()
        for song in soup.select("li.o-chart-results-list__item h3#title-of-a-story")
    ]
    return songs


def get_spotify():
    """Get an spotify object to update a playlist."""
    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-private",
        cache_path="token.txt",
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def get_track(spotify, song: str):  # type: ignore
    """Get track information."""
    try:
        return spotify.search(q=f"year:2025 track:{song}", type="track")["tracks"]["items"][0][  # type: ignore
            "uri"
        ]
    except:  # noqa: E722
        pass
    try:
        return spotify.search(q=f"year:2024 track:{song}", type="track")["tracks"]["items"][0][  # type: ignore
            "uri"
        ]
    except:  # noqa: E722
        return None


def main():
    """Main code logic."""
    # get_date()  # We will not end up using this given the website is now behind a pay wall
    resp = get_web_page()
    songs = get_top_100(resp)
    spotify = get_spotify()
    playlist = spotify.user_playlist_create(SPOTIFY_USER_ID, PLAYLIST_ID, public=False)  # type: ignore

    tracks = []
    for song in songs:
        track_uri = get_track(spotify, song)  # type: ignore
        if track_uri is not None:
            tracks.append(track_uri)  # type: ignore
    spotify.playlist_add_items(playlist["id"], tracks)  # type: ignore


if __name__ == "__main__":
    main()
