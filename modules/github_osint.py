import requests

HEADERS = {
    "User-Agent": "OSINT-Tool"
}

def search_github_username(username):
    url = f"https://api.github.com/search/issues?q={username}"
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        return[]
    
    data = response.json()
    results = [] 

    for item in data.get("items", [])[: 5]:
        results.append({
            "title": item["title"],
            "url": item["html_url"],
            "repository": item["repository_url"]
        })
    
    return results