import os
import smtplib
import time
from datetime import UTC, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv

MY_LAT = 36.850769
MY_LONG = -76.285873


def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    return (latitude, longitude)


def iss_within_5_degrees():
    """Your position is within +5/-5 degrees of the ISS position."""
    iss_lat, iss_long = get_iss_position()

    if abs(iss_lat - MY_LAT) < 5 and abs(iss_long - MY_LONG) < 5:
        return True
    else:
        return False


def get_sunset_sunrise():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters, verify=False
    )
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    return (sunset, sunrise)


def is_dark():
    sunset, sunrise = get_sunset_sunrise()
    current_hour = datetime.now(tz=UTC).hour

    if current_hour < sunrise or current_hour > sunset:
        return True
    else:
        return False


def send_email():
    load_dotenv()

    # Access environment variables
    sender = os.getenv("SENDER_EMAIL")
    credential = os.getenv("SENDER_CREDENTIAL")
    receiver = os.getenv("RECIPIENT_EMAIL")

    subject = "ISS Update"
    body = "Look up"

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to Outlook SMTP server and send email
    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(user=sender, password=credential)
            server.sendmail(
                from_addr=sender,
                to_addrs=receiver,
                msg=message.as_string(),
            )
    except Exception:
        print("Tried to send email... Logic worked!")


# If the ISS is close to my current position, and it is currently dark,
# then send me an email to tell me to look up.
# BONUS: Run the code every 60 seconds.
while True:
    if is_dark() and iss_within_5_degrees():
        send_email()

    time.sleep(60)
