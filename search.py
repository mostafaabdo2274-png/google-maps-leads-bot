from duckduckgo_search import DDGS


def search_places(query):
    parts = [x.strip() for x in query.split("|")]

    if len(parts) != 3:
        return []

    category = parts[0]
    city = parts[1]
    country = parts[2]

    searches = [
        f'site:yellowpages.com "{category}" "{city}" "{country}"',
        f'site:yellowpages.com.sa "{category}" "{city}"',
        f'site:daleeli.com "{category}" "{city}"',
        f'site:foursquare.com "{category}" "{city}"',
        f'"{category}" "{city}" "{country}"'
    ]

    results = []
    added = set()

    with DDGS() as ddgs:

        for q in searches:

            try:

                for r in ddgs.text(q, max_results=10):

                    url = r.get("href") or r.get("url")

                    if not url:
                        continue

                    if url in added:
                        continue

                    added.add(url)

                    results.append({
                        "name": r.get("title", ""),
                        "phone": "",
                        "website": url,
                        "address": r.get("body", ""),
                        "lat": "",
                        "lon": "",
                        "link": url
                    })

            except:
                pass

    return results
