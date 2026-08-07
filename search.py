import requests

from config import USER_AGENT, DEFAULT_RESULTS


def search_places(query: str):

    parts = [p.strip() for p in query.split("|")]

    if len(parts) != 3:
        return "❌ استخدم الأمر بالشكل التالي:\n/search النشاط | المدينة | الدولة"

    activity = parts[0]
    city = parts[1]
    country = parts[2]

    search_text = f"{activity}, {city}, {country}"

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": search_text,
        "format": "jsonv2",
        "limit": DEFAULT_RESULTS,
        "addressdetails": 1
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=20
    )

    if response.status_code != 200:
        return "❌ حدث خطأ أثناء الاتصال."

    data = response.json()

    if not data:
        return "❌ لا توجد نتائج."

    message = "📍 النتائج:\n\n"

    for i, item in enumerate(data[:10], 1):

        message += (
            f"{i}. {item.get('display_name')}\n"
            f"https://maps.google.com/?q={item['lat']},{item['lon']}\n\n"
        )

    return message
