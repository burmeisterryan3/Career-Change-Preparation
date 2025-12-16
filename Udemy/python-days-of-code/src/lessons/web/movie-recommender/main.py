"""Day 45 Challenge."""

from bs4 import BeautifulSoup
import requests

OUTPUT_FILE = "./movies.txt"
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
SELECTOR = "div.article-title-description__text h3.title"


def main():
    """Main logic."""
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = [movie.getText() for movie in soup.select(SELECTOR)]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for movie in reversed(movies):
            # Clean up this particular entry which is mislabeled
            if movie.split()[0] == "15)":
                movie = list(movie)
                movie[:3] = "80)"
                movie = "".join(movie)
            f.write(f"{movie}\n")


if __name__ == "__main__":
    main()
