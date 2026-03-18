import os
import sys

# Panggil config untuk pewarnaan terminal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def save_to_file(filename, domain, base_links, advanced_results=None):
    """
    Save results to a text file (.txt).
    Use a 'with open' block to free memory immediately after writing is complete..
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== {config.NAME} {config.VERSION} Report ===\n")
            f.write(f"Target : {domain}\n")
            f.write("=" * 45 + "\n\n")

            if advanced_results:
                f.write("[ Advanced Scan Results ]\n")
                f.write("Status | URL\n")
                f.write("-" * 45 + "\n")
                for url, status in advanced_results:
                    f.write(f"[{status}] {url}\n")
                f.write("-" * 45 + "\n")
                f.write(f"Total Endpoints: {len(advanced_results)}\n")
            
            else:
                f.write("[ Base Scan Results ]\n")
                f.write("Subdomains:\n")
                f.write("-" * 45 + "\n")
                for link in base_links:
                    f.write(f"{link}\n")
                f.write("-" * 45 + "\n")
                f.write(f"Total Subdomains: {len(base_links)}\n")

        print(f"{config.SUCCESS}[+] Results successfully saved to: {filename}{config.RESET}")
    
    except PermissionError:
        print(f"{config.ERROR}[-] Failed to save: Permission Denied. Check your folder rights.{config.RESET}")
    except Exception as e:
        print(f"{config.ERROR}[-] Failed to save results: {e}{config.RESET}")
