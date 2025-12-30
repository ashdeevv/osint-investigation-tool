import requests

HEADERS = {
    "User-Agent": "OSINT-Tool"
}

def search_github_email(email):
    query = f'"{email}"'
    url = f"https://api.github.com/search/code?q={query}"
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()
    results = []

    for item in data.get("items", [])[:5]:
        results.append({
            "file": item["name"],
            "repo": item["repository"]["full_name"],
            "url": item["html_url"]
        })

    return results
