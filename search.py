import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_places(query):

    parts = [x.strip() for x in query.split("|")]

    if len(parts) != 3:
        return []

    category, city, country = parts

    q = quote(f"{category} {city} {country}")

    url = f"https://html.duckduckgo.com/html/?q={q}"

    r = requests.get(url, headers=HEADERS, timeout=30)

    soup = BeautifulSoup(r.text, "lxml")

    results = []

    for item in soup.select(".result")[:20]:

        title = item.select_one(".result__title")

        link = item.select_one(".result__url")

        snippet = item.select_one(".result__snippet")

        results.append({

            "name": title.get_text(" ", strip=True) if title else "",

            "phone": "",

            "website": link.get_text(" ", strip=True) if link else "",

            "address": snippet.get_text(" ", strip=True) if snippet else "",

            "lat": "",

            "lon": "",

            "link": "https://" + link.get_text(strip=True).replace(" ", "") if link else ""

        })

    return results
