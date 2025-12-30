import requests
import re

HEADERS = {
    "User-Agent": "OSINT-Tool"
}

PHONE_REGEX = re.compile(
    r"(\+?\d{1,3}[\s\-]?)?(\(?\d{2,4}\)?[\s\-]?)?\d{3,4}[\s\-]?\d{3,4}"
)

def search_phone_in_github(username):
    url = f"https://api.github.com/search/code?q={username}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return []

        phones = set()

        for item in r.json().get("items", [])[:5]:
            file_url = item["url"]
            content = requests.get(file_url, headers=HEADERS).json()
            text = content.get("content", "")

            matches = PHONE_REGEX.findall(text)
            for m in matches:
                phone = "".join(m)
                if len(phone) >= 8:
                    phones.add(phone)

        return list(phones)
    except Exception:
        return []