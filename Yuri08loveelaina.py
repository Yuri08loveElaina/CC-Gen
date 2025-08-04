#!/usr/bin/env python3
import random
import requests
import sys
import os
import signal
import threading
import time
from datetime import datetime
from queue import Queue

# Terminal Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Ctrl+C handler
def sigint_handler(signal, frame):
    print(f"\n{RED}{BOLD}[!] Operation canceled by user{RESET}")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Banner
def print_banner():
    banner = f"""{CYAN}{BOLD}
    ELAINA CUTE | EXTENDED EDITION
    {RESET}
"""
    print(banner)

# Luhn Algorithm validation
def luhn_checksum(card_number: str) -> bool:
    def digits_of(n):
        return [int(d) for d in n]
    digits = digits_of(card_number)
    odd_sum = sum(digits[-1::-2])
    even_sum = 0
    for d in digits[-2::-2]:
        doubled = d * 2
        even_sum += doubled if doubled < 10 else doubled - 9
    return (odd_sum + even_sum) % 10 == 0

# Generate card number with valid Luhn checksum
def generate_card_number(bin_prefix: str, length=16):
    number = list(bin_prefix)
    while len(number) < (length - 1):
        number.append(str(random.randint(0,9)))
    # Calculate checksum digit
    for check_digit in range(10):
        candidate = ''.join(number) + str(check_digit)
        if luhn_checksum(candidate):
            return candidate
    return None  # Should never happen if algorithm correct

# yuri08loveelaina - check bin với proxy và delay tránh block API
def check_bin(pan, proxy=None):
    bin6 = pan[:6]
    if not bin6.isdigit() or len(bin6) != 6:
        return False, "INVALID", "N/A", "0", "UNKNOWN"
    
    headers = {
        'User-Agent': 'Yuri08-Elaina-Agent/2.5',  # yuri08loveelaina
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }
    
    proxies = {
        "http": proxy,
        "https": proxy
    } if proxy else None
    
    apis = [
        f"https://lookup.binlist.net/{bin6}",
        f"https://bins.su/api/{bin6}",
        f"https://bincheck.io/api/{bin6}",
        f"https://binlist.io/api/{bin6}"
    ]
    
    for url in apis:
        try:
            res = requests.get(url, headers=headers, timeout=5, proxies=proxies)
            if res.status_code == 200:
                data = res.json()
                # xử lý response tùy theo API
                if "lookup.binlist.net" in url:
                    scheme = data.get("scheme", "UNKNOWN").upper()
                    typ = data.get("type", "N/A").upper()
                    country = data.get("country", {}).get("name", "UNKNOWN")
                    emoji = data.get("country", {}).get("emoji", "🌐")
                    return True, scheme, typ, f"{emoji} {country}"
                elif "bins.su" in url:
                    info = None
                    if isinstance(data.get("data"), list):
                        info = data["data"][0] if len(data["data"]) > 0 else None
                    elif isinstance(data.get("data"), dict):
                        info = data["data"]
                    if info:
                        scheme = info.get("scheme", "UNKNOWN").upper()
                        typ = info.get("type", "N/A").upper()
                        country = info.get("country", "UNKNOWN")
                        return True, scheme, typ, country
                elif "bincheck.io" in url:
                    scheme = data.get("scheme", "UNKNOWN").upper()
                    typ = data.get("type", "N/A").upper()
                    country = data.get("country", "UNKNOWN")
                    return True, scheme, typ, country
                elif "binlist.io" in url:
                    scheme = data.get("scheme", "UNKNOWN").upper()
                    typ = data.get("type", "N/A").upper()
                    country = data.get("country", "UNKNOWN")
                    return True, scheme, typ, country
        except:
            pass
        
        # Delay ngẫu nhiên 0.5 - 1.5 giây giữa các API calls - yuri08loveelaina
        time.sleep(random.uniform(0.5, 1.5))
    
    return False, "N/A", "N/A", "🌐 UNKNOWN"

# Thread worker for checking cards
def worker(queue, results, mode, proxy):
    while True:
        card = queue.get()
        if card is None:
            break
        pan, mm, yy, cvv = card.split('|')[:4]
        valid_bin, scheme, typ, country = check_bin(pan, proxy)
        is_luhn_valid = luhn_checksum(pan)
        if mode == "strict":
            valid_card = valid_bin and is_luhn_valid
        else:
            valid_card = valid_bin
        status = "LIVE" if valid_card else "DEAD"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results.append((card, status, scheme, typ, country, timestamp))
        queue.task_done()

def generate_cards():
    clear_screen()
    print_banner()
    bin_input = input(f"{WHITE}Enter BIN (6 digits): {RESET}").strip()
    if len(bin_input) != 6 or not bin_input.isdigit():
        print(f"{RED}Invalid BIN! Must be 6 digits.{RESET}")
        return
    try:
        count = int(input(f"{WHITE}Number of cards to generate: {RESET}").strip())
        if count <= 0:
            print(f"{RED}Invalid number!{RESET}")
            return
    except:
        print(f"{RED}Invalid input!{RESET}")
        return

    save_file = input(f"{WHITE}Save to file (leave empty to skip): {RESET}").strip()

    print(f"\n{YELLOW}Generating {count} cards with valid Luhn checksum...{RESET}\n")

    cards = []
    for _ in range(count):
        pan = generate_card_number(bin_input)
        mm = str(random.randint(1, 12)).zfill(2)
        yy = str(random.randint(datetime.now().year % 100, 30))
        cvv = str(random.randint(100, 999))
        card = f"{pan}|{mm}|{yy}|{cvv}"
        cards.append(card)
        print(f"{GREEN}[+] {card}{RESET}")

    if save_file:
        with open(save_file, 'w') as f:
            f.write('\n'.join(cards))
        print(f"\n{GREEN}Cards saved to: {save_file}{RESET}")

def check_cards():
    clear_screen()
    print_banner()
    file_path = input(f"{WHITE}Enter card file path: {RESET}").strip()
    if not os.path.exists(file_path):
        print(f"{RED}File not found!{RESET}")
        return
    
    use_proxy = input(f"{WHITE}Use proxy? (y/N): {RESET}").strip().lower()
    proxy = None
    if use_proxy == 'y':
        proxy = input(f"{WHITE}Enter proxy (http://user:pass@ip:port or http://ip:port): {RESET}").strip()
        if not proxy:
            proxy = None

    print(f"{WHITE}Select check mode:{RESET}")
    print(f" 1 - Normal (BIN check only)")
    print(f" 2 - Strict (BIN + Luhn checksum)")
    mode_choice = input(f"{WHITE}Choice [1/2]: {RESET}").strip()
    mode = "strict" if mode_choice == "2" else "normal"

    output_live = "live_cards.txt"
    output_dead = "dead_cards.txt"
    output_log = "check_log.txt"
    live_count = 0
    dead_count = 0

    with open(file_path, 'r') as f:
        cards = [line.strip() for line in f if line.strip()]

    queue = Queue()
    results = []
    thread_count = 10

    # Start threads
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(queue, results, mode, proxy))
        t.daemon = True
        t.start()
        threads.append(t)

    # Enqueue cards
    for card in cards:
        if '|' not in card:
            print(f"{RED}Invalid format: {card}{RESET}")
            continue
        queue.put(card)

    # Block until all tasks done
    queue.join()

    # Stop workers
    for _ in range(thread_count):
        queue.put(None)
    for t in threads:
        t.join()

    # Write outputs and print summary
    with open(output_live, 'w') as livef, open(output_dead, 'w') as deadf, open(output_log, 'w') as logf:
        for card, status, scheme, typ, country, ts in results:
            pan = card.split('|')[0]
            line = f"{status} | {pan[:6]}...{pan[-4:]} | {scheme} | {typ} | {country} | {ts}\n"
            logf.write(line)
            if status == "LIVE":
                livef.write(card + "\n")
                live_count += 1
            else:
                deadf.write(card + "\n")
                dead_count += 1
            print(line.strip())

    print(f"\n{GREEN}Live cards: {live_count}{RESET}")
    print(f"{RED}Dead cards: {dead_count}{RESET}")
    print(f"{CYAN}Live cards saved to: {output_live}{RESET}")
    print(f"{YELLOW}Dead cards saved to: {output_dead}{RESET}")
    print(f"{CYAN}Check log saved to: {output_log}{RESET}")

def show_menu():
    clear_screen()
    print_banner()
    print(f"{CYAN}{BOLD}MAIN MENU:{RESET}")
    print(f"  {GREEN}1{RESET} - Generate CC with Luhn validation")
    print(f"  {GREEN}2{RESET} - Check CC from file (multithreaded)")
    print(f"  {RED}0{RESET} - Exit\n")

def main():
    while True:
        show_menu()
        choice = input(f"{WHITE}ELAINA> {RESET}").strip()
        if choice == "1":
            generate_cards()
        elif choice == "2":
            check_cards()
        elif choice == "0":
            print(f"\n{RED}Exiting ELAINA...{RESET}\n")
            break
        else:
            print(f"{RED}Invalid choice!{RESET}")
        input(f"\n{WHITE}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{RED}Fatal error: {str(e)}{RESET}")
        sys.exit(1)
