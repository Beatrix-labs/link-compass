import urllib.request
import urllib.error
import urllib.parse
import json
import socket
import concurrent.futures
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def fetch_crtsh(domain, timeout):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=timeout) as response:
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
                    print(f"{config.SUCCESS}[+] crt.sh engine found {len(subdomains)} subdomains.{config.RESET}")
                    return subdomains
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"{config.WARN}[!] crt.sh timed out. Retrying ({attempt+1}/{max_retries})...{config.RESET}")
                time.sleep(2)
            else:
                print(f"{config.ERROR}[-] crt.sh engine failed after {max_retries} attempts: {e}{config.RESET}")
                
    return subdomains

def fetch_hackertarget(domain, timeout):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    subdomains = set()
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8').split('\n')
                    for line in data:
                        if ',' in line:
                            sub = line.split(',')[0].strip().lower()
                            if sub.endswith(domain):
                                subdomains.add(sub)
                    print(f"{config.SUCCESS}[+] HackerTarget engine found {len(subdomains)} subdomains.{config.RESET}")
                    return subdomains
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"{config.WARN}[!] HackerTarget timed out. Retrying ({attempt+1}/{max_retries})...{config.RESET}")
                time.sleep(2)
            else:
                print(f"{config.ERROR}[-] HackerTarget engine failed after {max_retries} attempts: {e}{config.RESET}")
                
    return subdomains

def fetch_alienvault(domain, timeout):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    subdomains = set()
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if 'passive_dns' in data:
                        for entry in data['passive_dns']:
                            hostname = entry.get('hostname', '').strip().lower()
                            if hostname.endswith(domain) and not hostname.startswith('*'):
                                subdomains.add(hostname)
                    print(f"{config.SUCCESS}[+] AlienVault engine found {len(subdomains)} subdomains.{config.RESET}")
                    return subdomains
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"{config.WARN}[!] AlienVault timed out. Retrying ({attempt+1}/{max_retries})...{config.RESET}")
                time.sleep(2)
            else:
                print(f"{config.ERROR}[-] AlienVault failed after {max_retries} attempts: {e}{config.RESET}")
                
    return subdomains

def fetch_wayback(domain, timeout):
    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&fl=original&collapse=urlkey&limit=10000"
    subdomains = set()
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    for row in data[1:]:
                        if row:
                            original_url = row[0]
                            parsed_url = urllib.parse.urlparse(original_url)
                            hostname = parsed_url.hostname
                            if hostname and hostname.endswith(domain):
                                clean_sub = hostname.split(':')[0].strip().lower()
                                subdomains.add(clean_sub)
                    print(f"{config.SUCCESS}[+] Wayback Machine engine found {len(subdomains)} subdomains.{config.RESET}")
                    return subdomains
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"{config.WARN}[!] Wayback Machine timed out. Retrying ({attempt+1}/{max_retries})...{config.RESET}")
                time.sleep(2)
            else:
                print(f"{config.ERROR}[-] Wayback Machine failed after {max_retries} attempts: {e}{config.RESET}")
                
    return subdomains

def check_dns(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return subdomain, ip
    except socket.gaierror:
        return subdomain, None
    except Exception:
        return subdomain, None

def run_base_scan(domain, max_threads, timeout=15, deep_scan=False):
    print(f"{config.INFO}[*] Initializing multi-source OSINT engines...{config.RESET}")
    
    raw_subdomains = set()
    
    engines = [fetch_crtsh, fetch_hackertarget, fetch_alienvault]
    
    if deep_scan:
        print(f"{config.INFO}[*] Deep Scan triggered! Powering up Wayback Machine...{config.RESET}")
        engines.append(fetch_wayback)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(engines)) as executor:
        future_to_engine = {executor.submit(engine, domain, timeout): engine.__name__ for engine in engines}
        
        for future in concurrent.futures.as_completed(future_to_engine):
            engine_name = future_to_engine[future]
            try:
                result = future.result()
                raw_subdomains.update(result)
            except Exception as e:
                print(f"{config.ERROR}[-] Exception in {engine_name}: {e}{config.RESET}")

    if not raw_subdomains:
        print(f"{config.WARN}[!] No subdomains found from any source. Exiting engine.{config.RESET}")
        return []

    print(f"{config.INFO}[*] Aggregated {len(raw_subdomains)} unique subdomains from all sources.{config.RESET}")
    print(f"{config.INFO}[*] Resolving DNS using {max_threads} threads...{config.RESET}")
    
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
