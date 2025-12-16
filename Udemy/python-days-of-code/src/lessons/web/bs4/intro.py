"""Day 45."""

from bs4 import BeautifulSoup, Tag


def main():
    """Main program logic."""
    with open("website.html") as f:
        contents = f.read()

    soup = BeautifulSoup(contents, "html.parser")
    # print(f"title tag: {soup.title}")
    # print(f"title content: {soup.title.string}")

    # print(soup.prettify())

    # print(f"first paragraph: {soup.p}")

    # all_anchor_tags = soup.find_all("a")
    # print(all_anchor_tags)
    # for tag in all_anchor_tags:
    #     if isinstance(tag, Tag):
    #         print(f"text: {tag.get_text()}")
    #         print(f"href: {tag.get('href')}")

    # heading = soup.find(name="h1", id="name")
    # print(heading)

    # section_heading = soup.find(name="h3", class_="heading")
    # print(section_heading)

    # company_url = soup.select_one("p a").get("href")
    # print(company_url)

    # name = soup.select_one("#name")
    # print(name)

    headings = soup.select(".heading")
    print(headings)  # prints a list


if __name__ == "__main__":
    main()
