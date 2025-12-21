"""Day 48 Challenge."""

from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.python.org"


def get_events(driver: webdriver.Chrome):
    """Get evens from python.org."""
    driver.get(URL)

    events = {}
    items = driver.find_elements(By.CSS_SELECTOR, ".event-widget li")
    for i, item in enumerate(items):
        date = item.find_element(By.TAG_NAME, "time").text
        year_element = item.find_element(By.CLASS_NAME, "say-no-more")
        # Use textContent since .text returns empty for hidden elements
        year = year_element.get_attribute("textContent")
        name = item.find_element(By.TAG_NAME, "a").text
        events[i] = {"time": year + date, "name": name}  # type: ignore
    print(events)


def main():
    """Main logic."""
    driver = webdriver.Chrome()
    get_events(driver)


if __name__ == "__main__":
    main()
