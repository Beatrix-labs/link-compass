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

SIGNATURES = {
    "GitHub Pages": b"There isn't a GitHub Pages site here.",
    "Heroku": b"No such app",
    "AWS S3": b"The specified bucket does not exist",
    "Fastly": b"Fastly error: unknown domain",
    "Pantheon": b"The edge you specified",
    "Tumblr": b"Whatever you were looking for doesn't currently exist at this address",
    "WordPress": b"Do you want to register",
    "Ghost": b"The thing you were looking for is no longer here",
    "Surge": b"project not found",
    "Helpjuice": b"We could not find what you're looking for.",
    "Webflow": b"The page you are looking for doesn't exist or has been moved"
}

def check_takeover(url):
    """Make a request and match the response with the signature takeover."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=config.TIMEOUT, context=ctx) as response:
            body = response.read()
    except urllib.error.HTTPError as e:
        try:
            body = e.read()
        except:
            return None
    except Exception:
        return None
        
    for provider, sig in SIGNATURES.items():
        if sig in body:
            return url, provider
    return None

def run(active_links, max_threads):
    print(f"{config.WARN}[!] Initiating Subdomain Takeover Scan on {len(active_links)} targets...{config.RESET}")
    target_urls = [f"http://{link}" for link in active_links] + [f"https://{link}" for link in active_links]
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(check_takeover, url): url for url in target_urls}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                url, provider = res
                print(f"{config.ERROR}[ VULNERABLE ] -> {url} [ {provider} Takeover Possible! ]{config.RESET}")
                results.append(res)
    
    print(f"{config.INFO}[*] Takeover Scan Completed. Found: {len(results)} potential takeovers.{config.RESET}")
    return results
