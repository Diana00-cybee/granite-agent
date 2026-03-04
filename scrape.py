import re

from validation import is_content_valid
from curl_cffi import requests
from bs4 import BeautifulSoup
from log import agent_logger


def scrape_url(url, max_chars=2500):
    try:
        agent_logger.info(f"Scraping URL: {url}")
        response = requests.get(url, impersonate="chrome120", timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
            element.extract()

        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)

        if not is_content_valid(text):
            return "[ERROR: The content of this page was blocked or not found. Skipping.]"

        if len(text) > max_chars:
            return text[:max_chars] + "... [Content Truncated]"
        return text

    except Exception as e:
        return f"[ERROR: Connection failed: {str(e)}]"
