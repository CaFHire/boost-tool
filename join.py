import os
import sys
import shutil

# Gerekli Python modülleri
REQUIRED_PYTHON_MODULES = [
    "requests", "colored", "pystyle", "datetime", "keyboard", "tls_client",
    "easygui", "colorama", "pynput", "websocket", "fake_useragent",
    "httpx", "emoji", "bs4", "discum==1.1.0", "discord"
]

# Gerekli NPM modülleri
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

    # node_modules klasörü yoksa, toplu kurulum yap
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

# Banner ve menü
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

# Program başlangıcı
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
