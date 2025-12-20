"""Day 47 Challenge."""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests

URL = "https://www.amazon.com/Cuisinart-419-18P-Contour-Stainless-Saucepan/dp/B002WPHUEA/"
OBJECT = "Cuisinart 2-Quart Pot"
TARGET_PRICE = 40.0
load_dotenv()


def get_price(soup: BeautifulSoup) -> float:
    """Get the price of the desired object."""
    dollars_element = soup.select_one(".a-price-whole")
    cents_element = soup.select_one(".a-price-fraction")

    if dollars_element is None or cents_element is None:
        raise ValueError("Price elements not found on page")

    dollars = dollars_element.find(string=True, recursive=False)
    cents = cents_element.find(string=True, recursive=False)
    return float(f"{dollars}.{cents}")


def send_email(price: float):
    """Send an email notification about a price below a target threshold."""
    # Access environment variables
    email = os.getenv("EMAIL_ADDRESS")
    credential = os.getenv("EMAIL_PASSWORD")
    smtp_address = os.getenv("SMTP_ADDRESS")

    # Validate environment variables
    if not email or not credential or not smtp_address:
        raise ValueError(
            "SMTP_ADDRESS, EMAIL_ADDRESS, EMAIL_PASSWORD environment variables must be set"
        )

    # Create the email
    message = MIMEMultipart()
    message["From"] = email
    message["To"] = email
    message["Subject"] = "Great Price! Buy Now!"
    body = f"The price of {OBJECT} has dropped below ${TARGET_PRICE:.2f} and is now ${price}! Buy now!\n{URL}"
    message.attach(MIMEText(body, "plain"))

    # Connect to Outlook SMTP server and send email
    try:
        print(f"Sending email to {email}...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(user=email, password=credential)
            server.sendmail(
                from_addr=email,
                to_addrs=email,
                msg=message.as_string(),
            )
    except Exception as e:
        print(f"Failed to send email: {e}")


def main():
    """Main code logic."""
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    price = get_price(soup)

    if price < TARGET_PRICE:
        send_email(price)


if __name__ == "__main__":
    main()
