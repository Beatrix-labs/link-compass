import urllib.request
import urllib.error
import json
import socket
import concurrent.futures
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def fetch_crtsh(domain):
    """Passively searching for subdomains via the Certificate Transparency Log (crt.sh)."""
    print(f"{config.INFO}[*] Querying crt.sh database for {domain}...{config.RESET}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=config.TIMEOUT + 5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for entry in data:
                    names = entry.get('name_value', '').split('\n')
                    for name in names:
                        clean_name = name.strip().lower()
                        if clean_name.startswith('*.'):
                            clean_name = clean_name[2:]
                        if clean_name.endswith(domain):
                            subdomains.add(clean_name)
        
        print(f"{config.SUCCESS}[+] Found {len(subdomains)} unique subdomains from crt.sh.{config.RESET}")
        return list(subdomains)
    except urllib.error.URLError as e:
        print(f"{config.ERROR}[-] Failed to fetch from crt.sh: {e.reason}{config.RESET}")
        return []
    except Exception as e:
        print(f"{config.ERROR}[-] Engine Error: {e}{config.RESET}")
        return []

def check_dns(subdomain):
    """Checking whether the subdomain is really Live (Resolve to IP)."""
    try:
        ip = socket.gethostbyname(subdomain)
        return subdomain, ip
    except socket.gaierror:
        return subdomain, None

def run_base_scan(domain, max_threads):
    """Orchestration function that will be called by link-compass.py."""
    raw_subdomains = fetch_crtsh(domain)
    
    if not raw_subdomains:
        print(f"{config.WARN}[!] No subdomains found to process. Exiting engine.{config.RESET}")
        return []

    print(f"{config.INFO}[*] Resolving DNS for {len(raw_subdomains)} subdomains using {max_threads} threads...{config.RESET}")
    
    active_subdomains = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_sub = {executor.submit(check_dns, sub): sub for sub in raw_subdomains}
        
        for future in concurrent.futures.as_completed(future_to_sub):
            sub, ip = future.result()
            if ip:
                active_subdomains.append(sub)
                print(f"{config.SUCCESS}[+] {sub} {config.INFO}[{ip}]{config.RESET}")

    print(f"{config.INFO}--------------------------------------------------{config.RESET}")
    print(f"{config.SUCCESS}[+] Total Active Subdomains: {len(active_subdomains)}{config.RESET}")
    return active_subdomains
