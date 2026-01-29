import requests
import urllib3
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from datetime import datetime

# Inisialisasi
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===========================
# GLOBAL VARIABLES
# ===========================
print_lock = threading.Lock()
total_tasks = 0
completed_tasks = 0
found_count = 0
current_target_display = "Starting..."

# ===========================
# DATABASE DEFAULT
# ===========================
DEFAULT_EXTENSIONS = ['.env', '.sql', '.bak', '.old', '.zip', '.php', '.log', '.json', '.tar.gz', '.txt']
DEFAULT_WORDLIST = [
    'wp-config.php.bak', '.env', 'database', 'db', 'backup', 'dump', 
    'config', 'web.config', 'storage', 'phpinfo.php', '.git/config', 
    'server', 'users', 'admin', 'passwords', 'connection', 'debug',
    'id_rsa', 'shadow', 'docker-compose.yml', 'config.yml', '.htaccess'
]

def print_banner():
    clear_screen = "\033[H\033[J"
    print(clear_screen)
    dragon = f"""
{Fore.RED}              __        _
{Fore.RED}            _/  \\    _ ( \\
{Fore.RED}           / \\   \\  / \\ \\ \\
{Fore.RED}          /   )   \\/   ) \\ \\    {Fore.YELLOW}F S C A N {Fore.CYAN}v1.0 (BETA)
{Fore.RED}         /   /     \\  /   ) )   {Fore.WHITE}The Sensitive File Hunter
{Fore.RED}      _  \\  /      |  \\  / /
{Fore.RED}     ( \\  \\/       |   \\/ /
{Fore.RED}      \\ \\  \\       /      /     {Fore.GREEN}Author: anmxploit
{Fore.RED}       \\ \\  \\     /      /
{Fore.RED}        \\ \\  )   (      /       {Fore.MAGENTA}"See Everything, Miss Nothing"
{Fore.RED}         \\ \\/     \\    /
{Fore.RED}          \\/       \\  /
{Fore.RED}                    \\/
===========================================================
____________________                  ____   ____________   
\_   _____/   _____/ ____ _____    ___\   \ /   /\_____  \  
 |    __) \_____  \_/ ___\\__  \  /    \   Y   /   _(__  <  
 |     \  /        \  \___ / __ \|   |  \     /   /       \ 
 \___  / /_______  /\___  >____  /___|  /\___/   /______  / 
     \/          \/     \/     \/     \/                \/  

===========================================================

{Fore.WHITE}============================================================
{Fore.YELLOW}DISCLAIMER: {Fore.WHITE}Tools ini murni untuk edukasi & pentesting legal.
{Fore.WHITE}============================================================
"""
    print(dragon)

def ask(question, default=None):
    prompt = f"{Fore.CYAN}[?] {question}"
    if default:
        prompt += f" {Fore.WHITE}(Default: {default})"
    prompt += f": {Fore.YELLOW}"
    ans = input(prompt).strip()
    return ans if ans else default

def update_status():
    global completed_tasks, total_tasks, found_count, current_target_display
    percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    status = (
        f"\r{Fore.BLUE}[*] Progress: {Fore.WHITE}{percent:.1f}% "
        f"{Fore.BLUE}| Hit: {Fore.GREEN}{found_count} "
        f"{Fore.BLUE}| Target: {Fore.WHITE}{completed_tasks}/{total_tasks} "
        f"{Fore.BLUE}| Path: {Fore.YELLOW}{current_target_display[:25]}..."
    )
    sys.stdout.write(status + " " * 5)
    sys.stdout.flush()

def print_found(msg, output_file):
    global found_count
    with print_lock:
        sys.stdout.write("\r" + " " * 120 + "\r")
        print(msg)
        with open(output_file, 'a') as f:
            f.write(msg + '\n')
        found_count += 1

def worker(url_target, payloads, output_file, timeout, allowed_statuses):
    global completed_tasks, current_target_display
    url_target = url_target.strip().rstrip('/')
    if not url_target.startswith('http'): url_target = 'https://' + url_target

    for path in payloads:
        current_target_display = path
        update_status()
        full_url = f"{url_target}/{path}"
        try:
            # allow_redirects=False biar bisa nangkep 301/302
            res = requests.get(full_url, verify=False, timeout=timeout, allow_redirects=False)
            status = res.status_code
            time_now = datetime.now().strftime("%H:%M:%S")

            if status in allowed_statuses:
                # Logic Warna & Label
                if status == 200:
                    if b'<html' in res.content[:100].lower(): continue # Skip fake 200
                    color, label = Fore.GREEN, "FOUND"
                elif status == 403: color, label = Fore.YELLOW, "FORBIDDEN"
                elif status == 401: color, label = Fore.CYAN, "UNAUTHORIZED"
                elif status in [301, 302]: color, label = Fore.MAGENTA, "REDIRECT"
                else: color, label = Fore.WHITE, f"HTTP {status}"

                size = len(res.content) if status == 200 else "N/A"
                msg = f"{color}[+] {label}! {Fore.WHITE}| {time_now} | Size: {size} | {full_url}"
                print_found(msg, output_file)
        except: pass
    
    with print_lock:
        completed_tasks += 1
        update_status()

def main():
    global total_tasks
    print_banner()
    
    mode = ask("Pilih Mode Scan (1. Single / 2. Mass)", default='1')
    targets = []
    if mode == '1':
        targets.append(ask("Masukkan URL Target"))
    else:
        list_file = ask("Masukkan file list target")
        try:
            with open(list_file, 'r') as f:
                targets = [l.strip() for l in f if l.strip()]
        except: sys.exit(f"{Fore.RED}[!] File Target Error!")

    wl_choice = ask("Wordlist (1. Default / 2. Custom)", default='1')
    ext_choice = ask("Ekstensi (1. Default / 2. Custom)", default='1')
    
    # --- LOGIC FILTER STATUS BARU ---
    print(f"\n{Fore.WHITE}--- Filter Status Code ---")
    print(f"{Fore.GREEN}1. {Fore.WHITE}Default Analysis (200, 401, 403, 301, 302)")
    print(f"{Fore.GREEN}2. {Fore.WHITE}Custom (Input manual, ex: 200,403)")
    st_choice = ask("Pilihanmu", default='1')

    if st_choice == '1':
        allowed_statuses = [200, 401, 403, 301, 302]
    else:
        raw_st = ask("Masukkan status code (pisah koma, ex: 200,404)")
        allowed_statuses = [int(s.strip()) for s in raw_st.split(',')]

    # Generator Payloads (Simple version for this snippet)
    base_words = DEFAULT_WORDLIST if wl_choice == '1' else [] # Add custom logic if needed
    exts = DEFAULT_EXTENSIONS if ext_choice == '1' else [] # Add custom logic if needed
    payloads = []
    for w in base_words:
        if '.' in w: payloads.append(w)
        else: 
            for e in exts: payloads.append(w+e)
    
    output_file = ask("Nama file output", default='result.txt')
    threads = int(ask("Threads", default='20'))
    total_tasks = len(targets)

    print(f"\n{Fore.YELLOW}[!] ENGINE RUNNING... Filtering: {allowed_statuses}\n")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for t in targets:
            executor.submit(worker, t, list(set(payloads)), output_file, 5, allowed_statuses)
            
    update_status()
    print(f"\n\n{Fore.CYAN}[✓] SCAN SELESAI. Total Found: {found_count} dalam {time.time()-start_time:.2f}s")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.RED}[!] ABORTED.")
