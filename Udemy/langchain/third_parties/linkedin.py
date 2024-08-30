# linkedin.py

import json
import os

import requests


def scrape_linkedin_profile(linkedin_url: str, mock: bool = True):
    """Scrapes LinkedIn profile information for a given name."""
    name = os.path.basename(linkedin_url)
    name = "eden-marco"  # Hardcoded to ensure tokens are not used
    fname = f"third_parties/__cache__/{name}.json"

    if os.path.exists(fname) and mock:
        with open(fname) as f:
            return json.load(f)

    # Scraping code here
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dict = {
        "Authorization": f'Bearer {os.environ["PROXYCURL_API_KEY"]}',
    }

    response = requests.get(
        api_endpoint,
        headers=header_dict,
        params={"url": linkedin_url},
    )

    assert (
        response.status_code == 200
    ), f"Failed to scrape LinkedIn profile: {response.text}"

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], None, "")
        and k not in ["people_also_viewed", "certifications"]
    }

    with open(fname, "w") as f:
        json.dump(data, f)

    return response.json()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    data = scrape_linkedin_profile("https://www.linkedin.com/in/eden-marco/")

    print(data)
