##################### Extra Hard Starting Project ######################
# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.


import datetime as dt
import os
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
sender = os.getenv("SENDER_EMAIL")
credential = os.getenv("SENDER_CREDENTIAL")


def get_letter() -> Path:
    """Return a random file name from the letter templates folder."""
    directory = Path(__file__).parent / "letter_templates"
    files = os.listdir(directory)
    return directory / random.choice(files)


def read_letter(path: Path):
    """Read the contents of the letter."""
    with open(path) as f:
        letter = f.read()
    return letter


def insert_name(content: str, name: str):
    """Insert the name into the letter."""
    return content.replace("[NAME]", name, 1)


def gen_body(name: str) -> str:
    """Get a random motivational quote."""
    letter_path = get_letter()
    letter_content = read_letter(letter_path)
    letter = insert_name(letter_content, name)
    return letter


if __name__ == "__main__":
    today = dt.datetime.today()
    friends = pd.read_csv(Path(__file__).parent / "birthdays.csv")

    #### UNCOMMENT WHEN READY TO RUN AGAINST ACTUAL DATES ####
    matches = friends[
        (friends["year"] == 1961)
        & (friends["month"] == 12)
        & (friends["day"] == 21)
    ]
    # matches = friends[
    #     (friends["year"] == today.year)
    #     & (friends["month"] == today.month)
    #     & (friends["day"] == today.day)
    # ]
    for index, row in matches.iterrows():
        receiver_name = row["name"]
        receiver_address = row["email"]

        # Email content
        subject = "Happy Birthday!"
        body = gen_body(receiver_name)

        # Create the email
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receiver_address
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        print(message)

        #### UNCOMMENT IF ONCE OAUTH IMPLEMENTED TO SEND EMAILS ####

        # Connect to Outlook SMTP server and send email
        # try:
        #     with smtplib.SMTP("smtp.office365.com", 587) as server:
        #         server.starttls()
        #         server.login(user=sender, password=credential)
        #         server.sendmail(
        #             from_addr=sender,
        #             to_addrs=receiver_address,
        #             msg=message.as_string(),
        #         )
        # except Exception as e:
        #     print(f"Failed to send email: {e}")
