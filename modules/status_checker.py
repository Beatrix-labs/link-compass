import urllib.request
import urllib.error
import ssl
import concurrent.futures
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TREASURE_KEYWORDS = ['admin', 'dev', 'staging', 'api', 'config', 'staff', 'portal', 'beta', 'cms', 'dummy']

def extract_tech(headers):
    """Helper function to extract Server and X-Powered-By from HTTP headers."""
    tech = []
    
    server = headers.get('Server')
    if server:
        tech.append(server.strip())
        
    powered_by = headers.get('X-Powered-By')
    if powered_by:
        tech.append(f"Powered by {powered_by.strip()}")
        
    return f" [ Tech: {', '.join(tech)} ]" if tech else ""

def fetch_status(url):
    """Check HTTP status code and extract technology headers using HEAD method."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, method='HEAD')
    
    try:
        with urllib.request.urlopen(req, timeout=config.TIMEOUT, context=ctx) as response:
            tech_str = extract_tech(response.info())
            return url, response.status, tech_str
            
    except urllib.error.HTTPError as e:
        tech_str = extract_tech(e.info())
        return url, e.code, tech_str
        
    except urllib.error.URLError:
        return url, 0, ""
    except Exception:
        return url, 0, ""

def run(active_links, max_threads):
    print(f"{config.WARN}[!] Passing {len(active_links)} links to Advanced Status Checker...{config.RESET}")
    
    target_urls = []
    for link in active_links:
        target_urls.append(f"http://{link}")
        target_urls.append(f"https://{link}")

    print(f"{config.INFO}[*] Probing {len(target_urls)} endpoints (HTTP & HTTPS) using {max_threads} threads...{config.RESET}")
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_url = {executor.submit(fetch_status, url): url for url in target_urls}
        
        for future in concurrent.futures.as_completed(future_to_url):
            url, status, tech_str = future.result()
            
            if status > 0:
                results.append((url, status))
                
                if status == 200:
                    color = config.SUCCESS
                elif status in [401, 403]:
                    color = config.WARN
                else:
                    color = config.ERROR

                is_interesting = any(key in url.lower() for key in TREASURE_KEYWORDS)
                prefix = f"{config.ERROR}[ INTERESTING ]{config.RESET} " if is_interesting else ""

                print(f"{prefix}{color}[ {status} ] -> {url}{config.INFO}{tech_str}{config.RESET}")

    print(f"{config.INFO}--------------------------------------------------{config.RESET}")
    print(f"{config.WARN}[!] Advanced Probing Completed.{config.RESET}")
    return results
