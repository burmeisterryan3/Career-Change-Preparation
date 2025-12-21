"""Day 48."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://www.wikipedia.org/"
# URL = "https://en.wikipedia.org/wiki/Main_Page"


def print_num_english_articles(driver: webdriver.Chrome):
    """Get the number of articles from the main page."""
    print(driver.find_elements(By.CSS_SELECTOR, "#articlecount a")[1].text)


def find_by_link_text(driver: webdriver.Chrome):
    """Find a tag by the link text and click it."""
    all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")
    all_portals.click()


def search_wiki(driver: webdriver.Chrome):
    """Search for 'Python' programmatically."""
    # Find all search inputs and get the visible/interactable one
    search = driver.find_element(By.NAME, value="search")
    search.send_keys("Python (programming language)", Keys.ENTER)


def search_wiki_en(driver: webdriver.Chrome):
    """Search for 'Python' programmatically."""
    # Wait for search input to be present
    wait = WebDriverWait(driver, 10)
    search = wait.until(ec.presence_of_element_located((By.NAME, "search")))
    print("Search element found")
    # Use JavaScript to set the value and trigger the search, bypassing interactability issues
    driver.execute_script("arguments[0].value = 'Python';", search)
    driver.execute_script("arguments[0].form.submit();", search)


def main():
    """Main logic."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)  # type: ignore
    driver.get(URL)

    # print_num_english_articles(driver)
    # find_by_link_text(driver)
    search_wiki(driver)
    # search_wiki_en(driver) # this was complicated & required Claude support to debug


# searchform > div > div > div.cdx-text-input.cdx-text-input--has-start-icon.cdx-text-input--status-default.cdx-search-input__text-input > input
if __name__ == "__main__":
    main()
