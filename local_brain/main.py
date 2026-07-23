import os
import uvicorn
import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm import get_llm
from rag import get_retriever
from pyngrok import ngrok
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

app = FastAPI(title="ALYA Local Brain API", version="1.0")

class ChatRequest(BaseModel):
    prompt: str

# Initialize components
llm = get_llm(use_ollama=False)
retriever = get_retriever()

# Setup LangChain Chain
template = """Answer the question based only on the following context provided by The Feeder.
If the answer is not in the context, you can use your general knowledge but mention it.

Context: {context}

Question: {question}
"""
prompt_template = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

if llm and retriever:
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )
else:
    rag_chain = None

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    if not rag_chain:
        raise HTTPException(status_code=500, detail="LLM or Retriever failed to initialize.")
    
    try:
        response = rag_chain.invoke(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "llm_connected": llm is not None, "pinecone_connected": retriever is not None}

if __name__ == "__main__":
    print("\n" + "="*70)
    print("[INFO] FastAPI Server is running locally on http://0.0.0.0:8000")
    print("[INFO] To get a Public URL, run: python local_brain/tunnel.py in another terminal!")
    print("="*70 + "\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
