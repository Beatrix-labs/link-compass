import urllib.request
import urllib.error
import ssl
import concurrent.futures
import sys
import os
import hashlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TREASURE_KEYWORDS = ['admin', 'dev', 'staging', 'api', 'config', 'staff', 'portal', 'beta', 'cms', 'dummy']

PROXY_SIGNATURES = {
    "Cloudflare": ["cf-ray", "cf-cache-status", "__cfduid"],
    "Varnish": ["x-varnish", "x-cache"],
    "Akamai": ["x-akamai-transformed", "x-cache-akamai"],
    "Nginx-Proxy": ["x-proxy-cache", "x-nginx-upstream"],
    "F5 BigIP": ["x-cnection", "x-wa-info"],
    "Amazon CloudFront": ["x-amz-cf-id", "x-amz-cf-pop"]
}

def extract_tech_and_proxy(headers):
    """Extract Server tech and identify Reverse Proxies."""
    tech = []
    proxy_found = ""
    
    server = headers.get('Server')
    if server: tech.append(server.strip())
        
    powered_by = headers.get('X-Powered-By')
    if powered_by: tech.append(f"Powered by {powered_by.strip()}")
        
    header_keys = [h.lower() for h in headers.keys()]
    for proxy_name, sigs in PROXY_SIGNATURES.items():
        if any(sig in header_keys for sig in sigs):
            proxy_found = f" [ Proxy: {proxy_name} ]"
            break

    tech_str = f" [ Tech: {', '.join(tech)} ]" if tech else ""
    return tech_str, proxy_found

def fetch_status(url):
    """GET request with 2048-byte limit for Hash and Length extraction."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='GET')
    try:
        response = urllib.request.urlopen(req, timeout=config.TIMEOUT, context=ctx)
        body = response.read(2048)
        status = response.status
        headers = response.info()
    except urllib.error.HTTPError as e:
        body = e.read(2048)
        status = e.code
        headers = e.headers
    except Exception:
        return url, 0, ""
    tech_str, proxy_str = extract_tech_and_proxy(headers)
    
    c_length = headers.get('Content-Length', str(len(body)))
    
    content_hash = hashlib.md5(body).hexdigest()[:6]
    
    advanced_info = f"{tech_str}{proxy_str} [ Size: {c_length} | Hash: {content_hash} ]"
    return url, status, advanced_info

def run(active_links, max_threads):
    print(f"{config.WARN}[!] Passing {len(active_links)} links to Advanced Status Checker...{config.RESET}")
    
    target_urls = [f"http://{link}" for link in active_links] + [f"https://{link}" for link in active_links]
    print(f"{config.INFO}[*] Probing {len(target_urls)} endpoints using {max_threads} threads...{config.RESET}")
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_url = {executor.submit(fetch_status, url): url for url in target_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url, status, advanced_info = future.result()
            if status > 0:
                results.append((url, status))
                color = config.SUCCESS if status == 200 else config.WARN if status in [401, 403] else config.ERROR
                prefix = f"{config.ERROR}[ INTERESTING ]{config.RESET} " if any(key in url.lower() for key in TREASURE_KEYWORDS) else ""
                
                print(f"{prefix}{color}[ {status} ] -> {url}{config.INFO}{advanced_info}{config.RESET}")
                
    return results
