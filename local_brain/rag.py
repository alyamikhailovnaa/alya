import os
import logging
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def get_retriever():
    """
    Initializes and returns a Pinecone retriever using Gemini embeddings.
    """
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or not index_name or not gemini_key:
        logger.error("Missing environment variables for Pinecone or Gemini.")
        return None
        
    try:
        # Use the older embedding model for 768 dimensions
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=gemini_key
        )
        
        vectorstore = PineconeVectorStore(
            index_name=index_name,
            embedding=embeddings,
            pinecone_api_key=api_key
        )
        
        # Return a retriever that fetches top 3 most relevant context chunks
        return vectorstore.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        logger.error(f"Failed to initialize Pinecone retriever: {e}")
        return None
