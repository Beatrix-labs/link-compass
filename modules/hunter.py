import urllib.request
import ssl
import concurrent.futures
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

PAYLOADS = {
    "/.env": [b"APP_ENV", b"DB_PASSWORD", b"APP_KEY"],
    "/.git/config": [b"[core]", b"repositoryformatversion"],
    "/phpinfo.php": [b"phpinfo()", b"<title>phpinfo()</title>"],
    "/docker-compose.yml": [b"version:", b"services:"],
    "/.ssh/id_rsa": [b"BEGIN OPENSSH PRIVATE KEY", b"BEGIN RSA PRIVATE KEY"]
}

def check_path(base_url, path, signatures):
    url = f"{base_url}{path}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=config.TIMEOUT, context=ctx) as response:
            if response.status == 200:
                body = response.read(2048)
                for sig in signatures:
                    if sig in body:
                        return url, path
    except:
        pass
    return None

def run(active_links, max_threads):
    print(f"{config.WARN}[!] Initiating Modul Hunter (Sensitive File Discovery)...{config.RESET}")
    target_urls = [f"https://{link}" for link in active_links]
    
    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for url in target_urls:
            for path, signatures in PAYLOADS.items():
                tasks.append(executor.submit(check_path, url, path, signatures))
        
        results = []
        for future in concurrent.futures.as_completed(tasks):
            res = future.result()
            if res:
                url, path = res
                print(f"{config.ERROR}[ CRITICAL ] -> Exposed {path} found at {url}{config.RESET}")
                results.append(res)
                
    print(f"{config.INFO}[*] Modul Hunter Completed. Found: {len(results)} critical files.{config.RESET}")
    return results
