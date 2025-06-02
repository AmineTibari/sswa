import itertools

import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
scraper = cloudscraper.create_scraper()


def extract_data(url):
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all("form")
    form_data = []

    for form in forms:
        inputs = form.find_all("input")
        action = form.get("action")
        method = form.get("method", "get").lower()
        data = {inp.get("name"): inp.get("value", '') for inp in inputs if inp.get("name")}
        form_data.append({"action": urljoin(url, action), "method": method, "fields": data})

    return form_data

