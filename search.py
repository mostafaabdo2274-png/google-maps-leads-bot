import requests

from config import DEFAULT_RESULTS, USER_AGENT


def search_places(query):

    parts = [x.strip() for x in query.split("|")]

    if len(parts) != 3:
        return "❌ استخدم:\n/search النشاط | المدينة | الدولة"

    category, city, country = parts

    search_query = f"{category} in {city}, {country}"

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

        if not data:
            return "❌ لم يتم العثور على نتائج."

        text = "📍 النتائج:\n\n"

        for i, item in enumerate(data, 1):

            lat = item.get("lat", "")
            lon = item.get("lon", "")

            name = item.get("name")
            if not name:
                name = item.get("display_name", "").split(",")[0]

            address = item.get("display_name", "")

            text += (
                f"{i}. {name}\n"
                f"📍 {address}\n"
                f"🗺 https://www.google.com/maps?q={lat},{lon}\n\n"
            )

        return text

    except Exception as e:
        print(e)
        return f"❌ حدث خطأ:\n{e}"
