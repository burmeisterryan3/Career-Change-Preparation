"""Day 45."""

from bs4 import BeautifulSoup
import requests


def main():
    """Main logic."""
    response = requests.get("https://news.ycombinator.com/news")
    web_page = response.text

    soup = BeautifulSoup(web_page, "html.parser")

    rows = soup.select("span.titleline > a")
    titles = [title.getText() for title in rows]
    links = [link.get("href") for link in rows]

    # Not all articles will have a score. Set the score to 0 in those cases
    scores: list[int] = []
    for subline in soup.select("td.subtext"):
        score_tag = subline.select_one("span.score")
        score = int(score_tag.getText().split()[0]) if score_tag else 0
        scores.append(score)

    max_element = scores.index(max(scores))
    print(f"title: {titles[max_element]}")
    print(f"score: {scores[max_element]}")
    print(f"link: {links[max_element]}")

    # print(f"Titles: {len(titles)}")
    # print(f"Scores: {len(scores)}")
    # print(f"Links: {len(links)}")


if __name__ == "__main__":
    main()
