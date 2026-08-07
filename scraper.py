import re
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_website(url):

    data = {
        "email": "",
        "phone": "",
        "facebook": "",
        "instagram": "",
        "linkedin": "",
        "whatsapp": ""
    }

    if not url:
        return data

    try:

        html = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        ).text

        soup = BeautifulSoup(html, "lxml")

        text = soup.get_text(" ", strip=True)

        # Emails
        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        if emails:
            data["email"] = emails[0]

        # Phones
        phones = re.findall(
            r"\+?\d[\d\-\s()]{7,}",
            text
        )

        if phones:
            data["phone"] = phones[0]

        # Social links
        for link in soup.find_all("a", href=True):

            href = link["href"]

            if "facebook.com" in href:
                data["facebook"] = href

            elif "instagram.com" in href:
                data["instagram"] = href

            elif "linkedin.com" in href:
                data["linkedin"] = href

            elif "wa.me" in href or "whatsapp" in href:
                data["whatsapp"] = href

    except Exception:
        pass

    return data
