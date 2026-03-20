import urllib.request
import urllib.error
import urllib.parse
import json
import socket
import concurrent.futures
import sys
import os
import random
import string

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def detect_wildcard(domain):
    """Detects Wildcard DNS by resolving a random non-existent subdomain."""
    random_sub = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    test_domain = f"{random_sub}.{domain}"
    try:
        ip = socket.gethostbyname(test_domain)
        print(f"{config.WARN}[!] Wildcard DNS detected! Subdomains resolving to {ip} will be filtered.{config.RESET}")
        return ip
    except socket.gaierror:
        return None

def fetch_crtsh(domain, timeout):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
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
    except Exception:
        pass
    return subdomains

def fetch_anubis(domain, timeout):
    url = f"https://jldc.me/anubis/subdomains/{domain}"
    subdomains = set()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for sub in data:
                    clean_name = sub.strip().lower()
                    if clean_name.endswith(domain):
                        subdomains.add(clean_name)
                print(f"{config.SUCCESS}[+] Anubis engine found {len(subdomains)} subdomains.{config.RESET}")
    except Exception:
        pass
    return subdomains

def fetch_hackertarget(domain, timeout):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    subdomains = set()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = response.read().decode('utf-8').split('\n')
                for line in data:
                    if ',' in line:
                        sub = line.split(',')[0].strip().lower()
                        if sub.endswith(domain):
                            subdomains.add(sub)
                print(f"{config.SUCCESS}[+] HackerTarget engine found {len(subdomains)} subdomains.{config.RESET}")
    except Exception:
        pass
    return subdomains

def fetch_wayback(domain, timeout):
    """Subdomain enumeration using Wayback Machine (Archive.org)."""
    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&collapse=urlkey"
    subdomains = set()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for i, entry in enumerate(data):
                    if i == 0: continue
                    full_url = entry[2]
                    sub = full_url.split('/')[0].split(':')[0].lower()
                    if sub.endswith(domain):
                        subdomains.add(sub)
                print(f"{config.SUCCESS}[+] Wayback engine found {len(subdomains)} subdomains.{config.RESET}")
    except Exception:
        pass
    return subdomains


def fetch_virustotal(domain, timeout):
    if not config.VIRUSTOTAL_API: return set()
    
    url = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains?limit=1000"
    subdomains = set()
    try:
        req = urllib.request.Request(url, headers={'x-apikey': config.VIRUSTOTAL_API})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for item in data.get('data', []):
                    sub = item.get('id', '').strip().lower()
                    if sub.endswith(domain):
                        subdomains.add(sub)
                print(f"{config.SUCCESS}[+] VirusTotal engine found {len(subdomains)} subdomains.{config.RESET}")
    except Exception:
        pass
    return subdomains

def fetch_securitytrails(domain, timeout):
    if not config.SECURITYTRAILS_API: return set()
    
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    subdomains = set()
    try:
        req = urllib.request.Request(url, headers={'APIKEY': config.SECURITYTRAILS_API})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for sub in data.get('subdomains', []):
                    full_sub = f"{sub}.{domain}".lower()
                    subdomains.add(full_sub)
                print(f"{config.SUCCESS}[+] SecurityTrails engine found {len(subdomains)} subdomains.{config.RESET}")
    except Exception:
        pass
    return subdomains

def fetch_alienvaulg(domain, timeout):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    subdomains = set()
    try:
       req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
       with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for entry in data.get('passive_dns', []):
                    sub = entry.get('hostname', '').strip().lower()
                    if sub.endswith(domain) and '*' not in sub:
                        subdomains.add(sub)
        print(f"{config.SUCCESS}[+] AlienVault engine found {len(subdomains)} subdomains.{config.RESET}")
    except Exception:
        pass
    return subdomains

def fetch_threatminer(domain, timeout):
    url = f"https://api.threatminer.org/v2/domain.php?q={domain}&rt=5"
    subdomains = set()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for sub in data.get('results', []):
                    sub_clean = sub.strip().lower()
                    if sub_clean.endswith(domain):
                        subdomains.add(sub_clean)
        print(f"{config.SUCCESS}[+] ThreatMiner engine found {len(subdomains)} subdomains.{config.RESET}")
    except Exception:
        pass
    return subdomains

def check_dns(sub, wildcard_ip):
    try:
        ip = socket.gethostbyname(sub)
        if wildcard_ip and ip == wildcard_ip:
            return sub, None
        return sub, ip
    except Exception:
        return sub, None

def run_base_scan(domain, max_threads, timeout, deep_scan=False):
    print(f"{config.INFO}[*] Initializing multi-source OSINT engines...{config.RESET}")
    
    wildcard_ip = detect_wildcard(domain)
    
    engines = [fetch_crtsh, fetch_anubis, fetch_hackertarget, fetch_alienvault, fetch_threatminer]
    raw_subdomains = set()

    if deep_scan:
        print(f"{config.WARN}[!] Deep Scan Active: Engaging Wayback Machine (This may take longer...){config.RESET}")
        engines.append(fetch_wayback)

    if getattr(config, 'VIRUSTOTAL_API', ""):
       engines.append(fetch_virustotal)
    if getattr(config, 'SECURITYTRAILS_API', ''):
       engines.append(fetch_securitytrails)

    raw_subdomains = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(engines)) as executor:
        future_to_engine = {executor.submit(engine, domain, timeout): engine.__name__ for engine in engines}
        for future in concurrent.futures.as_completed(future_to_engine):
            try:
                result = future.result()
                if result:
                    raw_subdomains.update(result)
            except Exception:
                pass

    if not raw_subdomains:
        print(f"{config.WARN}[!] No subdomains found.{config.RESET}")
        return []

    print(f"{config.INFO}[*] Aggregated {len(raw_subdomains)} unique subdomains. Resolving DNS...{config.RESET}")
    
    active_subdomains = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_sub = {executor.submit(check_dns, sub, wildcard_ip): sub for sub in raw_subdomains}
        for future in concurrent.futures.as_completed(future_to_sub):
            sub, ip = future.result()
            if ip:
                active_subdomains.append(sub)
                print(f"{config.SUCCESS}[+] {sub} {config.INFO}[{ip}]{config.RESET}")

    return active_subdomains
