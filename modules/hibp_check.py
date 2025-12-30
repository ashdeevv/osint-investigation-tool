import requests
import os

HIBP_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"

HEADERS = {
    "User-Agent": "OSINT-Project",
    "hibp-api-key": os.getenv("HIBP_API_KEY")
}

def check_email_breaches(email):
    response = requests.get(
        HIBP_URL.format(email),
        headers=HEADERS,
        params={"truncateResponse": False},
        timeout=10
    )

    if response.status_code == 400:
        return {"breached": False, "breaches": []}
    
    if response.status_code == 200:
        data = response.json()
        return {
            "breached": True,
            "breaches": [
                {
                    "name": breach["Name"],
                    "domain": breach["Domain"],
                    "date": breach["BreachDate"],
                    "data": breach["DataClass"]
                }
                for breach in data
            ]
        }
    return {
        "error": f"HIBP error {response.status_code}"
    }