# Project Alya: Architecture & Security Protocol

Project Alya is a highly modular, AI-first hybrid ecosystem built on Python and Node.js. It bridges the gap between active GitHub automation, targeted data ingestion, and intelligent RAG-based query handling.

---

## 🏗️ System Architecture (The Triad)

### 1. Component A: GitHub Automator (Badge Hunter)
- **Role**: Maintains daily GitHub activity (green dots) and hunts for specialized GitHub badges (e.g., Pull Shark, Quickdraw, YOLO) via automated bots.
- **Stack**: Node.js, GitHub Actions (`@octokit/rest`).
- **Data Flow**: Scheduled via Cron (`activity.yml`) -> Octokit SDK -> GitHub API -> Push/PR/Issue.

### 2. Component B: The Feeder
- **Role**: A low-resource worker that scrapes hyper-niche daily data (e.g., Anime News Network RSS), filters it using an AI Gatekeeper to ensure novelty, and ingests it into a Vector Database.
- **Stack**: Python, BeautifulSoup (Scraping), Google Gemini API (Gatekeeper), Pinecone (VectorDB).
- **Data Flow**: `scraper.py` -> `gatekeeper.py` (Gemini 3.5 Flash) -> `embedder.py` (Gemini-embedding-001) -> Pinecone Index (768 Dimensions).

### 3. Component C: The Local Brain
- **Role**: A REST API layer running locally that orchestrates LangChain, RAG, and LLMs to serve intelligent responses based on the data ingested by The Feeder.
- **Stack**: Python, FastAPI, LangChain, Localtunnel (via Node.js).
- **Data Flow**: User Prompt -> FastAPI Endpoint -> LangChain Retriever (Pinecone) -> Context Injection -> LLM (Gemini 3.5 Flash / Local Ollama) -> JSON Response.

---

## 🛡️ Security Audit & Rules (Strictly Enforced)

Because this repository is **PUBLIC**, the following rules are non-negotiable and have been audited:

1. **Secret Management**:
   - The `.env` file and Python environments (`venv/`, `venv_brain/`, `__pycache__/`) are explicitly tracked in `.gitignore`.
   - **Rule**: NEVER hardcode API keys. Always use `os.getenv("KEY")` in Python or `process.env.KEY` in Node.js.

2. **Log Sanitization**:
   - The GitHub Action logs are fully public.
   - **Rule**: NEVER print raw API responses or full stack traces (`e` or `err`). All `catch` and `except` blocks MUST emit sanitized, generic error messages (e.g., `[ERROR] Automation failed: <short_message>`).

3. **Polite Web Scraping**:
   - **Rule**: The scraper must always identify itself clearly to avoid being flagged as a malicious bot. `requests.get()` headers must include `"User-Agent": "ProjectChimera-Bot/1.0"`.

4. **Dimension Safety**:
   - Pinecone Vector dimensions must perfectly align with the embedding model.
   - **Rule**: `gemini-embedding-001` generates **768 Dimensions**. Ensure the Pinecone index is always set to 768.

---

## 🔧 Maintenance Notes

**Switching the LLM Engine (Gemini -> Local Ollama)**
If you wish to switch from the cloud Gemini API back to your local RTX 3060 running Ollama, follow these steps:
1. Ensure Ollama is installed and running (`ollama run llama3.1`).
2. Run `pip install langchain-ollama` in your `venv_brain`.
3. In `local_brain/main.py`, simply pass `use_ollama=True` to the `get_llm()` initialization. The code will automatically route all queries to your local GPU!
