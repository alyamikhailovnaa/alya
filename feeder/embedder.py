import os
import logging
import hashlib
import time
from pinecone import Pinecone
from google import genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def embed_and_store(items):
    """
    Generates embeddings for the items and stores them in Pinecone.
    """
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or not index_name or not gemini_key:
        logger.error("Missing Pinecone or Gemini API keys in environment.")
        return False
        
    logger.info(f"Connecting to Pinecone index: {index_name}")
    try:
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)
    except Exception as e:
        logger.error(f"Pinecone connection error: {e}")
        return False

    client = genai.Client(api_key=gemini_key)
    vectors = []
    
    for item in items:
        text_to_embed = f"Title: {item['title']}\n\nContent: {item['content']}"
        try:
            # Menggunakan model embedding lama yang berukuran 768 dimensi
            response = client.models.embed_content(
                model='gemini-embedding-001',
                contents=text_to_embed
            )
            embedding = response.embeddings[0].values
            
            # Unique ID based on link or title
            doc_id = hashlib.md5(item['link'].encode('utf-8')).hexdigest()
            
            vectors.append({
                "id": doc_id,
                "values": embedding,
                "metadata": {
                    "title": item['title'],
                    "link": item['link'],
                    "pub_date": item['pub_date'],
                    "text": item['content']
                }
            })
            
        except Exception as e:
            logger.error(f"Error embedding item '{item['title']}': {e}")
            
        time.sleep(2)
            
    if vectors:
        try:
            index.upsert(vectors=vectors)
            msg = f"[BERHASIL] Mengirim {len(vectors)} data ke index Pinecone '{index_name}'!"
            logger.info(msg)
            print(msg)
            return True
        except Exception as e:
            err = f"[ERROR] Gagal mengirim data ke Pinecone: {e}"
            logger.error(err)
            print(err)
            return False
    else:
        msg = "[INFO] Tidak ada data baru yang lolos Gatekeeper hari ini. (0 data dikirim ke Pinecone)"
        logger.info(msg)
        print(msg)
        return True
