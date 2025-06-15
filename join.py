import os
import sys
import shutil
import requests
import hashlib

# ========== Güncelleme Ayarları ==========

GITHUB_USER = "CaFHire"
REPO_NAME = "boost-tool"
BRANCH = "main"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}"

PROTECTED = [
    "node_modules", "programlar", "pyarmor_runtime_000000",
    "config.json", "package-lock.json", "proxies.txt", "tokens.txt"
]

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def hash_content(content):
    return hashlib.sha256(content).hexdigest()

def update_file(file_path):
    print(f"\n[🔍] {file_path} kontrol ediliyor...")
    try:
        url = f"{RAW_BASE_URL}/{file_path}"
        r = requests.get(url)
        if r.status_code != 200:
            print(f"[!] {file_path} uzaktan alınamadı: {r.status_code}")
            return

        remote = r.content
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(remote)
            print(f"[+] {file_path} indirildi.")
            return

        local_hash = hash_file(file_path)
        remote_hash = hash_content(remote)

        if local_hash != remote_hash:
            with open(file_path, "wb") as f:
                f.write(remote)
            print(f"[✓] {file_path} güncellendi.")
        else:
            print(f"[=] {file_path} zaten güncel.")
    except Exception as e:
        print(f"[HATA] {file_path} güncelleme hatası: {e}")

def remove_unwanted_files():
    for item in os.listdir():
        if item in PROTECTED:
            continue
        if item.endswith(".py") or os.path.isdir(item) or item.endswith(".json") or item.endswith(".txt"):
            try:
                response = requests.get(f"{RAW_BASE_URL}/{item}")
                if response.status_code == 404:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                    print(f"[🧹] Eski dosya silindi: {item}")
            except:
                continue

def check_for_updates():
    print("╔══════════════════════════════════════════╗")
    print("║      🔄 CAFO Tool Auto-Updater v3.0      ║")
    print("╚══════════════════════════════════════════╝")
    update_file("join.py")
    remove_unwanted_files()
    print("\n[✓] Güncelleme tamamlandı.\n")

check_for_updates()

# ========== Python ve NPM Modül Kurulumu ==========

REQUIRED_PYTHON_MODULES = [
    "requests", "colored", "pystyle", "datetime", "keyboard", "tls_client",
    "easygui", "colorama", "pynput", "websocket", "fake_useragent",
    "httpx", "emoji", "bs4", "discum==1.1.0", "discord"
]

REQUIRED_NPM_MODULES = [
    "2captcha",
    "chalk",
    "gradient-string",
    "discord.js-selfbot-v13",
    "discord.js-selfbot-v13-proxy",
    "https-proxy-agent",
    "proxy-agent"
]

def install_python_modules():
    for module in REQUIRED_PYTHON_MODULES:
        try:
            __import__(module.split("==")[0])
        except ModuleNotFoundError:
            print(f"📦 Python modülü yükleniyor ➜ {module}")
            os.system(f'pip install {module}')

def install_npm_modules():
    if shutil.which("node") is None or shutil.which("npm") is None:
        print("❌ Node.js ve npm yüklü değil veya PATH'e tanımlı değil.")
        input("Devam etmek için bir tuşa bas...")
        sys.exit()

    print("✅ Node.js ve npm tespit edildi.")

    if not os.path.exists("node_modules"):
        print("📂 'node_modules' klasörü yok. Tüm modüller yükleniyor...")
        os.system("npm install")

    for module in REQUIRED_NPM_MODULES:
        mod_path = os.path.join("node_modules", module.split("/")[-1])
        if not os.path.exists(mod_path):
            print(f"📦 NPM modülü yükleniyor ➜ {module}")
            os.system(f"npm install {module}")
        else:
            print(f"✅ NPM modülü zaten yüklü ➜ {module}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ========== Arayüz ==========
def display_banner():
    from pystyle import Colorate, Colors
    print(Colorate.Horizontal(Colors.rainbow, """
 ██████╗ █████╗ ███████╗██╗  ██╗██╗██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝██║  ██║██║██╔══██╗██╔════╝
██║     ███████║█████╗  ███████║██║██████╔╝█████╗  
██║     ██╔══██║██╔══╝  ██╔══██║██║██╔══██╗██╔══╝  
╚██████╗██║  ██║██║     ██║  ██║██║██║  ██║███████╗
 ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
    """))
    print("")
    print(Colorate.Horizontal(Colors.yellow_to_red, "              🔗 Token Join & Boost Tool 🔗\n"))

def display_menu():
    from colorama import Fore
    print(Fore.GREEN + """
   [1] ➜ Join Server
   [2] ➜ Boost Server
   [exit] ➜ Çıkış
""")

def execute_command(command):
    if command in ['1', '2']:
        os.system('cmd /k "node boost.js"' if os.name == 'nt' else 'node boost.js')
    else:
        from colorama import Fore
        print(Fore.RED + "❌ Lütfen geçerli bir seçenek girin!")

# ========== Ana Program ==========
if __name__ == "__main__":
    install_python_modules()
    install_npm_modules()
    while True:
        clear_screen()
        display_banner()
        display_menu()
        from colorama import Fore
        command = input(Fore.YELLOW + "> ").strip().lower()
        if command == "exit":
            print(Fore.CYAN + "👋 Çıkılıyor...")
            break
        execute_command(command)
