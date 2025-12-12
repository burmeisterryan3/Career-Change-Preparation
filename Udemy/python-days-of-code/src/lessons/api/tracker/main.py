import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

URL_PREFIX = "https://pixe.la/"
TOKEN = os.getenv("PIXELA_TOKEN")
USERNAME = "ryan641171"
GRAPH_ID = "graph1"


def submit_request(url, request_type, payload=None, headers=None):
    try:
        if request_type == "post":
            response = requests.post(url, json=payload, headers=headers)
        elif request_type == "put":
            response = requests.put(url, json=payload, headers=headers)
        else:  # request_type == "delete" returns True
            response = requests.delete(url, headers=headers)

        # Check for success
        if response.status_code in (200, 201, 204):
            print(f"✅ Success! Status code: {response.status_code}")
            # If there's a JSON response, parse it safely
            try:
                data = response.json()
                print("Response JSON:", data)
            except ValueError:
                print("No JSON in response.")
        else:
            print(f"❌ Failed. Status code: {response.status_code}")
            print("Response text:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request error: {e}")


def create_user():
    payload = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }

    url = URL_PREFIX + "v1/users"
    submit_request(url, payload)


def get_profile(filename="profile.html"):
    url = URL_PREFIX + f"@{USERNAME}"
    resp = requests.get(url=url)
    out_file = os.path.join(
        os.getcwd(), "days_of_code", "lessons", "api", "tracker", f"{filename}"
    )
    with open(out_file, "w") as f:
        f.write(resp.text)


def create_graph():
    url = URL_PREFIX + f"v1/users/{USERNAME}/graphs"

    headers = {"X-USER-TOKEN": TOKEN}

    payload = {
        "id": "graph1",
        "name": "upskilling",
        "unit": "hours",
        "type": "float",
        "color": "shibafu",
    }
    submit_request(url, "post", payload, headers=headers)


def post_pixel(graph_id, dt=None, quantity=1):
    """Dt must be in the format yyyyMMdd. quantity is in hours."""
    url = URL_PREFIX + f"v1/users/{USERNAME}/graphs/{graph_id}"

    if dt is None:
        dt = datetime.now().strftime("%Y%m%d")

    headers = {"X-USER-TOKEN": TOKEN}

    payload = {
        "date": dt,
        "quantity": str(quantity),
    }

    submit_request(url, "post", payload, headers=headers)


def update_pixel(graph_id: str, dt: str, quantity: str):
    url = URL_PREFIX + f"/v1/users/{USERNAME}/graphs/{graph_id}/{dt}"
    headers = {"X-USER-TOKEN": TOKEN}
    payload = {"quantity": quantity}
    submit_request(url, payload, request_type="put", headers=headers)


def delete_pixel(graph_id, dt):
    url = URL_PREFIX + f"/v1/users/{USERNAME}/graphs/{graph_id}/{dt}"
    headers = {"X-USER-TOKEN": TOKEN}
    submit_request(url, "delete", headers=headers)


if __name__ == "__main__":
    # create_user()
    # get_profile()
    # create_graph()
    # post_pixel(GRAPH_ID)
    # update_pixel(
    #     graph_id=GRAPH_ID,
    #     dt=datetime(year=2025, month=11, day=12).strftime("%Y%m%d"),
    #     quantity=str(1.5),
    # )
    delete_pixel(
        graph_id=GRAPH_ID,
        dt=datetime(year=2025, month=11, day=12).strftime("%Y%m%d"),
    )
