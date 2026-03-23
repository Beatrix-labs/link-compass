> Archive: I'm focusing more on active Bug Hunting research.

# Link-Compass

**Developed by Beatrix Labs**

Link-Compass is a lightning-fast, zero-bloat passive reconnaissance and HTTP probing tool designed for Bug Bounty Hunters and Security Researchers. 

Built entirely upon Python's standard libraries, Link-Compass requires zero external dependencies. It is engineered to perform rapid subdomain enumeration and status code checking without the overhead of heavy third-party packages, making it exceptionally lightweight and highly scalable.

## Why Link-Compass?

Many reconnaissance tools rely on heavy web-request libraries that download entire page contents just to check if a server is alive, leading to high bandwidth usage and slower execution times. Link-Compass solves this by:
1. **Zero-Bloat Architecture:** Utilizing only native Python libraries (`urllib`, `socket`, `concurrent.futures`).
2. **Passive Discovery:** Querying Certificate Transparency logs (`crt.sh`) without directly touching the target's primary infrastructure.
3. **Smart Probing:** Utilizing HTTP `HEAD` requests to verify status codes (200, 403, 404) instantly without downloading page bodies.
4. **Native Multithreading:** Executing highly concurrent DNS resolution and HTTP probing safely and efficiently.

## Features

- **Multi-Engine OSINT:** Queries 8+ sources including `crt.sh`, `Anubis`, `HackerTarget`, `AlienVault`, `ThreatMiner`, and `Wayback Machine`.
- **Premium Intelligence:** Optional integration with **VirusTotal** and **SecurityTrails** API for enterprise-grade discovery.
- **Wildcard Defense:** Smart DNS filtering to eliminate "garbage" subdomains from wildcard configurations.
- **Advanced Probing:** Not just status codes, but also **Content Size**, **MD5 Hashing**, and **Tech Stack** identification.
- **Infrastructure Profiling:** Detects Reverse Proxies (Cloudflare, Akamai, etc.) and Server headers out-of-the-box.
- **Vulnerability Modules:** Integrated **Subdomain Takeover** and **Sensitive File Hunter** (/.env, /.git).
- **Zero-Bloat:** 100% Native Python. No `pip install`, no heavy dependencies, works perfectly on Termux.

## Prerequisites

- Python 3.x
- An active internet connection
- *No `pip install` required.*

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/Beatrix-labs/link-compass.git
cd link-compass
```

## Global Setup (Run from anywhere)

To run `link-compass` globally from any directory without needing the `python` or `./` prefix, you need to make the script executable and create a symbolic link to your system's binaries.

**For Linux/macOS:**

```bash
chmod +x link-compass.py
sudo ln -s $(pwd)/link-compass.py /usr/local/bin/link-compass
```

**For Termux(Android):**

```bash
chmod +x link-compass.py
ln -s $(pwd)/link-compass.py $PREFIX/bin/link-compass
```

You can now use the tool by simply typing `link-compass` anywhere in your terminal.

## Usage

Link-Compass is built with a modular approach. It operates in a lightweight base mode by default, and expands its capabilities only when specific flags are passed.

**Basic Reconnaissance (Discovery Only)**

This mode quickly fetches and resolves subdomains without sending HTTP requests to them.

```bash
link-compass -d target.com
```

**Advanced Probing (Status Checker & Export)**

This mode activates the status checker module, probing both port 80 and 443, utilizing multiple threads, and saving the organized results to a file.

```bash
link-compass -d target.com --status -t 30 -o output.txt
```

## Available Arguments

| Flag | Name | Description | Required |
| :--- | :--- | :--- | :--- |
| -d | --domain | The target domain (e.g., example.com) | Yes |
| -s | --status | Enable HTTP status code checking (200, 403, 404) | No |
| -t | --threads | Number of concurrent threads (Default: 10) | No |
| -o | --output | Save the final output to a specified text file | No |
| -j | --json | Export the final result to a structured JSON file | No |
| --timeout | --timeout | Custom timeout for API requests in seconds (Default: 15) | No |
| --deep | --deep | Enable deep scan using Wayback Machine (slower but comprehensive) | No |
| --takeover | --takeover | Scan for Subdomain Takeover vulnerabilities | No |
| --hunter | --hunter | Hunt for sensitive files (/.env, /.git, etc.) | No |

## Project Architecture

The codebase is strictly modular to ensure easy maintenance and scalability:

- `/core/`: Contains the primary passive reconnaissance engine and DNS resolution logic.
- `/modules/`: Houses advanced capabilities, such as the HTTP status checker, which are only invoked when requested by the user.
- `/utils/`: Contains operational utilities like the automated file reporter and native terminal styling.

## Contributing

Beatrix Labs welcomes contributions from the open-source community. If you have ideas to improve the tool without compromising the "zero-bloat" philosophy, follow these steps:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code relies solely on standard Python libraries.

## Disclaimer

This tool is developed for educational purposes, authorized security auditing, and Bug Bounty hunting. The developers at Beatrix Labs assume no liability and are not responsible for any misuse or damage caused by this program. Always ensure you have explicit permission to test a target.

## License

Distributed under the MIT License.

