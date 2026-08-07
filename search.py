from duckduckgo_search import DDGS


def search_places(query):

    parts = [x.strip() for x in query.split("|")]

    if len(parts) != 3:
        return []

    category = parts[0]
    city = parts[1]
    country = parts[2]

    search = f"{category} {city} {country}"

    results = []

    try:

        with DDGS() as ddgs:

            for r in ddgs.text(
                search,
                max_results=20
            ):

                url = r.get("href") or r.get("url")

                if not url:
                    continue

                results.append({

                    "name": r.get("title", ""),

                    "phone": "",

                    "website": url,

                    "address": r.get("body", ""),

                    "lat": "",

                    "lon": "",

                    "link": url

                })

    except Exception as e:

        print(e)

    return results
