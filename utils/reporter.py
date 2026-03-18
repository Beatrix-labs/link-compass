import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def export_json(domain, subdomains, probed_endpoints=None, filename="output.json"):
    """
    Zero-Bloat JSON exporter.
    Converts raw reconnaissance data into a highly structured JSON format.
    """
    report_data = {
        "metadata": {
            "target": domain,
            "tool": "Link-Compass",
            "version": "0.1.0"
        },
        "reconnaissance": {
            "total_active_subdomains": len(subdomains),
            "subdomains": subdomains
        }
    }

    if probed_endpoints:
        formatted_endpoints = []
        for url, status in probed_endpoints:
            formatted_endpoints.append({
                "url": url,
                "status_code": status
            })
            
        report_data["advanced_probing"] = {
            "total_endpoints_scanned": len(formatted_endpoints),
            "results": formatted_endpoints
        }

    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(report_data, json_file, indent=4)
        print(f"{config.SUCCESS}[+] JSON report successfully saved to: {filename}{config.RESET}")
    except Exception as e:
        print(f"{config.ERROR}[-] Failed to generate JSON report: {e}{config.RESET}")
