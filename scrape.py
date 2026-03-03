import re

from curl_cffi import requests
from bs4 import BeautifulSoup
from log import agent_logger


def scrape_url(url, max_chars=1500):
    """Fetches webpage using advanced browser impersonation."""
    try:
        agent_logger.info(f"Scraping URL for deep context: {url}\n")
        
        response = requests.get(
            url, 
            impersonate="chrome120", 
            timeout=8
        )
        
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
            element.extract()

        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)

        if len(text) > max_chars:
            return text[:max_chars] + "... [Content Truncated]"
            
        return text if text else "No readable text found on page."

    except Exception as e:
        agent_logger.error(f"Failed to scrape {url}: {str(e)}")
        return f"[Content blocked by website security: {str(e)}. Rely on the search snippet instead.]"

