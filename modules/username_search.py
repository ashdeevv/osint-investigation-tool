import requests

SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "Medium": "https://medium.com/@{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (OSINT Tool)"
}

def search_username(username):
    results = {}

    for site, url in SITES.items():
        try:
            response = requests.get(
                url.format(username),
                headers=HEADERS,
                timeout=5
            )

            if response.status_code == 200 and username.lower() in response.text.lower():
                results[site] = True
            else:
                results[site] = False

        except requests.RequestException:
            results[site] = False

    return results