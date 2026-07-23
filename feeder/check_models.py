import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
r = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}")
data = r.json()
if 'models' in data:
    for m in data['models']:
        print(f"{m['name']} - {m.get('supportedGenerationMethods', [])}")
else:
    print(data)
