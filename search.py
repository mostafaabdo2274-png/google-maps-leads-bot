import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_places(query):

    parts = [x.strip() for x in query.split("|")]

    if len(parts) != 3:
        return []

    category = parts[0]
    city = parts[1]
    country = parts[2]

    q = f"{category} {city} {country}"

    url = f"https://www.yellowpages.com/search?search_terms={q}"

    r = requests.get(url, headers=HEADERS, timeout=30)

    soup = BeautifulSoup(r.text, "lxml")

    results = []

    cards = soup.select(".result")

    for card in cards[:20]:

        try:

            name = card.select_one(".business-name").get_text(strip=True)

        except:
            continue

        phone = ""

        p = card.select_one(".phones")

        if p:
            phone = p.get_text(strip=True)

        address = ""

        a = card.select_one(".street-address")

        if a:
            address = a.get_text(" ", strip=True)

        website = ""

        w = card.select_one(".track-visit-website")

        if w:
            website = w.get("href", "")

        results.append({
            "name": name,
            "phone": phone,
            "website": website,
            "address": address,
            "lat": "",
            "lon": "",
            "link": website
        })

    return results
