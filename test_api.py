import requests
import json
import sys

def main():
    print("="*60)
    print("🤖 TERMINAL CHAT AI - THE LOCAL BRAIN 🤖")
    print("="*60)
    
    # Meminta URL dari user
    print("Masukkan Public URL Anda (yang berakhiran loca.lt)")
    print("Contoh: https://punya-saya.loca.lt")
    base_url = input("URL: ").strip()
    
    # Hapus trailing slash jika ada
    if base_url.endswith("/"):
        base_url = base_url[:-1]
        
    chat_url = f"{base_url}/api/v1/chat"
    
    print("\n[INFO] Menghubungkan ke The Local Brain...")
    
    # Test koneksi dengan ping endpoint /health
    try:
        health = requests.get(f"{base_url}/health")
        if health.status_code == 200:
            print("[INFO] Koneksi Berhasil! ✅\n")
        else:
            print("[WARNING] URL bisa diakses tapi The Local Brain merespon dengan error.\n")
    except Exception as e:
        print(f"[ERROR] Tidak dapat terhubung ke URL tersebut. Pastikan tunnel menyala. ({e})")
        sys.exit(1)
        
    print("Silakan mengobrol! (Ketik 'keluar' atau 'exit' untuk berhenti)\n")
    print("-" * 60)
    
    while True:
        prompt = input("\nAnda: ")
        if prompt.lower() in ['keluar', 'exit', 'quit']:
            print("Sampai jumpa! 👋")
            break
            
        if not prompt.strip():
            continue
            
        payload = {
            "prompt": prompt
        }
        
        try:
            print("Memikirkan jawaban...")
            response = requests.post(chat_url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                sources = data.get('sources', [])
                
                print(f"\nAI: {answer}")
                
                if sources:
                    print("\n[Sumber Pengetahuan yang Dibaca AI dari Pinecone]:")
                    for i, src in enumerate(sources, 1):
                        print(f"{i}. {src.get('title', 'Unknown Title')}")
            else:
                print(f"\n[ERROR Server]: Kode {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"\n[ERROR Jaringan]: {e}")

if __name__ == "__main__":
    main()
