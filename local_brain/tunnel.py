import os
import subprocess

def start_tunnel():
    print("\n" + "="*70)
    print("[INFO] Starting Localtunnel (via Node.js)...")
    print("[INFO] Tunggu beberapa saat, Anda akan mendapatkan URL: 'https://....loca.lt'")
    print("[INFO] Itu adalah Public URL API Anda yang bisa diakses dari mana saja!")
    print("="*70 + "\n")
    
    try:
        subprocess.run(["npx", "localtunnel", "--port", "8000"], shell=True)
    except Exception as e:
        print(f"[ERROR] Gagal menjalankan localtunnel: {e}")

if __name__ == "__main__":
    start_tunnel()
