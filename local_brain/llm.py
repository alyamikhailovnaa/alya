import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def get_llm(use_ollama=False):
    """
    Returns an instance of the LLM.
    Change `use_ollama=True` in main.py whenever you are ready to switch back to Local Llama!
    """
    try:
        if use_ollama:
            logger.info("Using Local Ollama (llama3.1)")
            try:
                from langchain_ollama import ChatOllama
            except ImportError:
                raise ImportError("Please run `pip install langchain-ollama` to use Ollama.")
            return ChatOllama(model="llama3.1", base_url="http://localhost:11434")
        else:
            logger.info("Using Cloud Gemini API")
            gemini_key = os.getenv("GEMINI_API_KEY")
            # Menggunakan gemini-3.5-flash sesuai dengan model yang tersedia di API Key Anda
            return ChatGoogleGenerativeAI(model="gemini-3.5-flash", google_api_key=gemini_key)
            
    except Exception as e:
        logger.error(f"Failed to connect to LLM: {e}")
        return None
