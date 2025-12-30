import requests

def find_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        subdomains = set()

        for entry in data:
            names = entry["name_value"].split("\n")
            for name in names:
                if name.endswith(domain):
                    subdomains.add(name.strip())

        return list(subdomains)
    except Exception:
        return []