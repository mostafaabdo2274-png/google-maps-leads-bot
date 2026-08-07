import requests

from config import DEFAULT_RESULTS, USER_AGENT


def search_places(query):

    parts = [x.strip() for x in query.split("|")]

    if len(parts) != 3:
        return []

    category = parts[0]
    city = parts[1]
    country = parts[2]

    search_query = f"{category}, {city}, {country}"

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": search_query,
        "format": "jsonv2",
        "limit": DEFAULT_RESULTS,
        "addressdetails": 1
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data:

            lat = item.get("lat", "")
            lon = item.get("lon", "")

            results.append({

                "name": item.get("name") or item.get("display_name", "").split(",")[0],

                "phone": "",

                "website": "",

                "address": item.get("display_name", ""),

                "lat": lat,

                "lon": lon,

                "link": f"https://www.google.com/maps?q={lat},{lon}"

            })

        return results

    except Exception as e:

        print(e)

        return []
