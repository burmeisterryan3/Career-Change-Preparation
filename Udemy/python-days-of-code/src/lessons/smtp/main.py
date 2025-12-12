import datetime as dt
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv


def gen_quote() -> str:
    """Get a random motivational quote."""
    try:
        with open("./days_of_code/lessons/smtp/quotes.txt") as f:
            return random.choice(f.readlines())
    except Exception:
        return "Good luck! -Ryan"


if __name__ == "__main__":
    # Load environment variables from the .env file
    load_dotenv()

    # Access environment variables
    sender = os.getenv("SENDER_EMAIL")
    credential = os.getenv("SENDER_CREDENTIAL")
    receiver = os.getenv("RECIPIENT_EMAIL")

    if dt.datetime.today().strftime("%A") == "Friday":
        # Email content
        subject = "Motivational Quote"
        body = gen_quote()

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
        except Exception as e:
            print(f"Failed to send email: {e}")
