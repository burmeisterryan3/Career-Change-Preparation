"""Day 48."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def run_amazon(driver: webdriver.Chrome):
    """Run a driver for an Amazon product."""
    driver.get(
        "https://www.amazon.com/Pragmatic-Programmer-journey-mastery-Anniversary/dp/0135957052/"
    )

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    product_title = wait.until(
        expected_conditions.presence_of_element_located((By.ID, "productTitle"))
    )

    # Find all price elements and get the first visible one
    price_wholes = driver.find_elements(By.CLASS_NAME, "a-price-whole")
    price_fractions = driver.find_elements(By.CLASS_NAME, "a-price-fraction")

    # Filter for visible elements with non-empty text
    price_dollar = None
    price_cents = None

    for elem in price_wholes:
        if elem.is_displayed() and elem.text.strip():
            price_dollar = elem
            break

    for elem in price_fractions:
        if elem.is_displayed() and elem.text.strip():
            price_cents = elem
            break

    if price_dollar and price_cents:
        print(f"The price of {product_title.text} is ${price_dollar.text}.{price_cents.text}.")
    else:
        print(
            f"Could not find price. Found {len(price_wholes)} whole price elements and {len(price_fractions)} fraction elements."
        )
        # Debug: print all found prices
        for i, elem in enumerate(price_wholes):
            print(f"Price whole {i}: visible={elem.is_displayed()}, text='{elem.text}'")


def run_python_org(driver: webdriver.Chrome):
    """Run a driver for an Amazon product."""
    driver.get("https://www.python.org")
    search_bar = driver.find_element(By.NAME, value="q")
    print(search_bar.tag_name)
    placeholder = search_bar.get_attribute("placeholder")  # type: ignore
    print(placeholder)
    button = driver.find_element(By.ID, value="submit")
    print(button.size)
    documentation_link = driver.find_element(By.CSS_SELECTOR, ".documentation-widget a")
    print(documentation_link.text)
    bug_link = driver.find_element(By.XPATH, '//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
    print(bug_link.get_attribute("href"))


def main():
    """Main logic."""
    # Keep the browser open even after the script finishes running
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)  # type: ignore

    driver = webdriver.Chrome(options=chrome_options)
    # run_amazon(driver)
    run_python_org(driver)
    driver.quit()


if __name__ == "__main__":
    main()
