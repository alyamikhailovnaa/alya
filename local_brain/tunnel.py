import os
import urllib.request
import subprocess

def start_tunnel():
    exe_path = "cloudflared.exe"
    if not os.path.exists(exe_path):
        print("Downloading cloudflared.exe for Quick Tunnels...")
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
        urllib.request.urlretrieve(url, exe_path)
    
    print("\n" + "="*70)
    print("[INFO] Starting Cloudflare Quick Tunnel...")
    print("[INFO] Cari baris yang mengandung tulisan: 'https://....trycloudflare.com'")
    print("[INFO] Itu adalah Public URL API Anda yang bisa diakses dari mana saja!")
    print("="*70 + "\n")
    
    # Run cloudflared without requiring an account
    subprocess.run([exe_path, "tunnel", "--url", "http://localhost:8000"])

if __name__ == "__main__":
    start_tunnel()
