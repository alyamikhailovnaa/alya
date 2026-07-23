import os
import time
from google import genai
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def filter_data(items):
    """
    Passes items through the AI Gatekeeper to ensure they are novel (post May 2024).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("No GEMINI_API_KEY found.")
        return []
        
    client = genai.Client(api_key=api_key)
    filtered = []
    
    logger.info(f"Passing {len(items[:5])} items through the Gatekeeper (with 15s rate limiting)...")
    
    # Process only the top 5 items to fit within strict free tier constraints for this test
    for item in items[:5]:
        prompt = f"""
        Analyze this news item:
        Title: {item['title']}
        Content: {item['content']}
        
        Is the core subject of this news globally known or released BEFORE May 2024?
        Reply with exactly 'YES' if it is known before May 2024.
        Reply with exactly 'NO' if this is new information (after May 2024).
        """
        try:
            # Using valid model from 2026 available to this key
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
            )
            answer = response.text.strip().upper()
            
            if 'NO' in answer:
                msg = f"[PASSED] Data lolos Gatekeeper: {item['title']}"
                logger.info(msg)
                print(msg)
                filtered.append(item)
            else:
                msg = f"[REJECTED] Topik sudah lama/umum: {item['title']}"
                logger.info(msg)
                print(msg)
        except Exception as e:
            err = f"[ERROR] Gatekeeper error pada '{item['title']}': {e}"
            logger.error(err)
            print(err)
            
        # Sleep to respect strict free tier rate limit
        time.sleep(15)
            
    return filtered
