import requests
import logging
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Target: Anime News Network RSS (or any niche feed)
RSS_URL = "https://www.animenewsnetwork.com/news/rss.xml"

def scrape_data():
    """
    Fetches latest niche news from the RSS feed.
    Returns a list of dictionaries with 'title', 'link', 'description', 'pub_date'.
    """
    logger.info(f"Fetching RSS feed from {RSS_URL}...")
    try:
        headers = {"User-Agent": "ProjectChimera-Bot/1.0"}
        response = requests.get(RSS_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch RSS. Request aborted.")
        return []

    try:
        root = ET.fromstring(response.content)
    except Exception as e:
        logger.error(f"Failed to parse XML: {e}")
        return []
        
    items = root.findall('.//item')
    scraped_items = []
    
    for item in items:
        title_el = item.find('title')
        link_el = item.find('link')
        desc_el = item.find('description')
        pub_date_el = item.find('pubDate')
        
        title = title_el.text if title_el is not None else ""
        link = link_el.text if link_el is not None else ""
        description = desc_el.text if desc_el is not None else ""
        pub_date = pub_date_el.text if pub_date_el is not None else ""
        
        # Clean up description (remove HTML tags inside description if any)
        clean_desc = BeautifulSoup(description, 'html.parser').get_text(strip=True) if description else ""
        
        scraped_items.append({
            "title": title,
            "link": link,
            "content": clean_desc,
            "pub_date": pub_date
        })

    logger.info(f"Scraped {len(scraped_items)} items from feed.")
    return scraped_items

if __name__ == "__main__":
    # Test execution
    data = scrape_data()
    for d in data[:2]:
        print(d)
