import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 1. Set up the Chrome WebDriver
# This automatically downloads and manages the correct ChromeDriver version
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # type: ignore
driver = webdriver.Chrome()

try:
    # 2. Open the Wikipedia homepage
    driver.get("https://www.wikipedia.org/")
    print("Navigated to Wikipedia homepage")

    # 3. Locate the search input field
    # The search input field can be located by its 'name' attribute, which is 'search'
    search_input = driver.find_element(By.NAME, "search")
    print("Located the search input field")

    # 4. Enter a search term and submit the search
    search_input.send_keys("Selenium (software)")
    search_input.send_keys(Keys.RETURN)  # Simulate pressing the Enter key
    print("Entered search term and submitted")

    # 5. Wait for a few seconds to see the results page (optional, for observation)
    time.sleep(5)
    print(f"Current page title: {driver.title}")

finally:
    # 6. Close the browser
    driver.quit()
