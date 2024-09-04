import os
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

visited_urls = set()


def download_html(url: str, base_url: str, folder: Path):
    """Download HTML files from the given URL and save them in the folder."""
    if url in visited_urls:
        return
    visited_urls.add(url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        file_name = folder.joinpath(Path(url.replace(base_url, "")))

        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(soup.prettify())

        for link in soup.find_all("a", href=True):
            href = link["href"]

            if href.endswith(".html") and not (
                href.startswith("http") or href.startswith("..")
            ):
                if base_url not in href:
                    href = urljoin(url, href)

                download_html(href, base_url, folder)


if __name__ == "__main__":
    prefix = "https://python.langchain.com/v0.2/"
    download_folder = "./langchain-docs/"

    # Does not include ecosystem or versions from docs
    for loc in [
        "api_reference/",
        "docs/introduction",
        "docs/tutorials",
        "docs/how_to",
        "docs/concepts",
        "docs/security",
    ]:
        url = urljoin(prefix, loc)
        if loc == "api_reference/":
            download_html(
                urljoin(url, "index.html"),
                url,
                Path(download_folder + loc),
            )
        else:
            download_html(url, prefix, Path(download_folder))
