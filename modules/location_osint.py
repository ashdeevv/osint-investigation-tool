import requests

HEADERS = {
    "User-Agent": "OSINT-Tool"
}

def search_location_from_github(username):
    url = f"https://api.github.com/users/{username}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return "Non déterminé"

        data = r.json()
        location = data.get("location")

        if location:
            return location

        return "Non renseigné publiquement"

    except Exception:
        return "Erreur"
