import logging
import os
import datetime
from scraper import scrape_data
from gatekeeper import filter_data
from embedder import embed_and_store

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting The Feeder pipeline...")
    
    # 1. Scrape data
    raw_items = scrape_data()
    if not raw_items:
        logger.warning("No data scraped. Exiting.")
        return

    # 2. Filter data via AI Gatekeeper
    novel_items = filter_data(raw_items)
    if not novel_items:
        logger.info("No novel items passed the gatekeeper today. Exiting.")
        return

    # 3. Embed and store in Vector DB
    success = embed_and_store(novel_items)
    
    # 4. Generate daily log for GitHub activity
    if success:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        log_path = os.path.join(log_dir, f"ingested_{date_str}.md")
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"# Ingestion Log: {date_str}\n\n")
            f.write(f"Successfully ingested {len(novel_items)} novel items.\n\n")
            for item in novel_items:
                f.write(f"- **{item['title']}**\n")
                f.write(f"  - Link: {item['link']}\n")
                
        logger.info(f"Ingestion log written to {log_path}")
    else:
        logger.error("Pipeline failed during embedding/storage phase.")

if __name__ == "__main__":
    main()
