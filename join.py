import os
import sys
import shutil
import requests
import hashlib

# ===============================
# 🔒 KORUNAN DOSYA VE KLASÖRLER
# ===============================
PROTECTED = [
    "node_modules", "programlar", "pyarmor_runtime_000000",
    "config.json", "package-lock.json", "proxies.txt", "tokens.txt"
]

# ===============================
# 📦 GEREKLİ MODÜLLER
# ===============================
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

# ===============================
# 🔧 PYTHON MODÜLLERİ KURULUMU
# ===============================
def install_python_modules():
    for module in REQUIRED_PYTHON_MODULES:
        try:
            __import__(module.split("==")[0])
        except ModuleNotFoundError:
            print(f"📦 Python modülü yükleniyor ➜ {module}")
            os.system(f'pip install {module}')

# ===============================
# 🔧 NPM MODÜLLERİ KURULUMU
# ===============================
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

# ===============================
# 🔁 HASH YARDIMCILARI
# ===============================
def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def hash_content(content):
    return hashlib.sha256(content).hexdigest()

# ===============================
# 🌐 GITHUB GÜNCELLEME
# ===============================
GITHUB_USER = "CaFHire"
REPO_NAME = "boost-tool"
BRANCH = "main"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}"
API_BASE_URL = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents?ref={BRANCH}"

def check_for_updates():
    print("╔══════════════════════════════════════════╗")
    print("║      🔄 CAFO Tool Auto-Updater v3.0      ║")
    print("╚══════════════════════════════════════════╝")

    try:
        r = requests.get(API_BASE_URL)
        if r.status_code != 200:
            print(f"[!] GitHub API erişim hatası: {r.status_code}")
            return

        github_files = r.json()
        github_filenames = []

        for file in github_files:
            if file["type"] != "file":
                continue

            filename = file["name"]
            github_filenames.append(filename)

            if filename in PROTECTED:
                print(f"[🔒] Atlaniyor (korunan): {filename}")
                continue

            raw_url = file["download_url"]
            r2 = requests.get(raw_url)
            if r2.status_code != 200:
                print(f"[!] {filename} indirilemedi: {r2.status_code}")
                continue

            remote_content = r2.content
            remote_hash = hash_content(remote_content)

            if not os.path.exists(filename):
                with open(filename, "wb") as f:
                    f.write(remote_content)
                print(f"[+] {filename} indirildi.")
            else:
                local_hash = hash_file(filename)
                if local_hash != remote_hash:
                    with open(filename, "wb") as f:
                        f.write(remote_content)
                    print(f"[✓] {filename} güncellendi.")
                else:
                    print(f"[=] {filename} zaten güncel.")

        # Fazlalıkları sil
        for file in os.listdir():
            if file in PROTECTED or file in github_filenames:
                continue
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    print(f"[🧹] Silindi: {file}")
                elif os.path.isdir(file):
                    shutil.rmtree(file)
                    print(f"[🧹] Klasör silindi: {file}")
            except Exception as e:
                print(f"[!] Silinemedi: {file} ({e})")

        print("\n[✓] Güncelleme tamamlandı.\n")

    except Exception as e:
        print(f"[!] Güncelleme kontrolü başarısız: {e}")

# ===============================
# 🧹 EKRANI TEMİZLE
# ===============================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ===============================
# 🎨 ARAYÜZ
# ===============================
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
    print(Colorate.Horizontal(Colors.yellow_to_red, "              🔗 Token Join & Boost Tool Version 1.3 🔗\n"))

def display_menu():
    from colorama import Fore
    print(Fore.GREEN + """
   [1] = Join Server
   [2] = Boost Server
   [exit] = Çıkış
""")

def execute_command(command):
    if command in ['1', '2']:
        os.system('cmd /k "node boost.js"' if os.name == 'nt' else 'node boost.js')
    else:
        from colorama import Fore
        print(Fore.RED + "❌ Lütfen geçerli bir seçenek girin!")

# ===============================
# 🚀 PROGRAM BAŞLANGICI
# ===============================
if __name__ == "__main__":
    check_for_updates()
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
    