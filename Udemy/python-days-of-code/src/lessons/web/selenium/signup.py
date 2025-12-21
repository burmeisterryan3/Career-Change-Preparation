"""Day 48 Signup."""

from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://secure-retreat-92358.herokuapp.com/"


def main():
    """Main logic."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(URL)
    # This solution works
    # fname = driver.find_element(By.NAME, "fName")
    # fname.send_keys("test", Keys.TAB, "test", Keys.TAB, "test@testing.com", Keys.TAB, Keys.ENTER)

    # This solution allows for more practice
    # Find the fields
    fname = driver.find_element(By.NAME, "fName")
    lname = driver.find_element(By.NAME, "lName")
    email = driver.find_element(By.NAME, "email")
    # Fill out the form
    fname.send_keys("Test")
    lname.send_keys("Test")
    email.send_keys("Test@testing.com")
    # Locate the "Sign Up" button and click
    submit = driver.find_element(By.CSS_SELECTOR, "form button")
    submit.click()


if __name__ == "__main__":
    main()
