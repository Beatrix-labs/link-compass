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

def fetch_status(url):
    """Check HTTP status code using HEAD method to make it super light."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
    
    try:
        with urllib.request.urlopen(req, timeout=config.TIMEOUT, context=ctx) as response:
            return url, response.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except urllib.error.URLError:
        return url, 0
    except Exception:
        return url, 0

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
            url, status = future.result()
            
            if status > 0:
                results.append((url, status))
                
                if status == 200:
                    color = config.SUCCESS
                elif status in [401, 403]:
                    color = config.WARN
                else:
                    color = config.ERROR

                print(f"{color}[ {status} ] -> {url}{config.RESET}")

    print(f"{config.INFO}--------------------------------------------------{config.RESET}")
    print(f"{config.WARN}[!] Advanced Probing Completed.{config.RESET}")
    return results
