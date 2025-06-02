from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import json

# --- CONFIGURATION ---
SUCCESS_KEYWORDS = ["welcome", "dashboard", "admin", "logged in", "success", "bienvenue", "connecté", "connexion réussie"]
ERROR_KEYWORDS = ["sql syntax", "mysql", "error in your sql", "warning", "pdoexception", "syntax error"]
FORBIDDEN_KEYWORDS = ["forbidden", "access denied", "blocked"]
TIMEOUT_THRESHOLD = 5



# --- UTILS ---
def calculate_difference_ratio(before_text, after_text):
    matcher = SequenceMatcher(None, before_text, after_text)
    similarity_ratio = matcher.ratio()
    difference_percentage = (1 - similarity_ratio) * 100
    return round(difference_percentage, 2)

def advanced_compare(before_html, after_html):
    before_soup = BeautifulSoup(before_html, 'html.parser')
    after_soup = BeautifulSoup(after_html, 'html.parser')
    return {
        "tag_diff": abs(len(before_soup.find_all()) - len(after_soup.find_all())),
        "title_changed": before_soup.title != after_soup.title,
        "content_length_diff": abs(len(before_html) - len(after_html)),
        "has_sql_error": any(kw in after_html.lower() for kw in ERROR_KEYWORDS)
    }

def analyze_response(before_response, after_response, injected_fields, payload):
    status = after_response.status_code
    before = before_response.text.lower()
    after = after_response.text.lower()
    diff = calculate_difference_ratio(before, after)
    meta = advanced_compare(before_response.text, after_response.text)

    result = { "fields": injected_fields, "payload": payload, "status": status, "difference": diff, "analysis": meta, "vulnerable": False, "severity": "Low" }

    if status == 200 and (
            diff > 10 or
            meta["has_sql_error"]
            or any(kw in after for kw in SUCCESS_KEYWORDS)
    ):
        result["vulnerable"] = True
        result["severity"] = "High" if meta["has_sql_error"] else "Medium"
    elif status in [403, 401] or any(kw in after for kw in FORBIDDEN_KEYWORDS):
        result["severity"] = "Medium"
    elif status in [301, 302]:
        result["severity"] = "Low"

    return result

