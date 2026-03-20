# Changelog

All notable changes to **Link-Compass** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-03-20

### Added
- **Premium API Integration**: Added support for VirusTotal and SecurityTrails via API keys in `config.py`.
- **New OSINT Engines**: Integrated AlienVault OTX and ThreatMiner for broader passive discovery.
- **Wildcard DNS Filtering**: Automatic detection and filtering of catch-all IP addresses to prevent false positives.
- **Advanced Status Probing**: Added extraction of Response Size (`Content-Length`) and a 6-char MD5 Hash for page deduplication.
- **Reverse Proxy Detection**: Automated identification of Cloudflare, Akamai, Varnish, and more via header signatures.

### Changed
- Increased `MAX_THREADS` default to 20 for better performance on stable connections.
- Optimized `urllib` requests with custom User-Agent to reduce blocks from API providers.
- Updated JSON report versioning for better integration with external tools.

## [0.3.0] - 2026-03-19

### Added
- **Modul Hunter (`--hunter`)**: Added a highly efficient scanner for discovering sensitive exposed files (`/.env`, `/.git/config`, etc.) using signature matching.
- **Subdomain Takeover Scanner (`--takeover`)**: Added capability to detect dangling subdomains pointing to inactive cloud services (e.g., AWS S3, GitHub Pages, Heroku).

### Changed
- Replaced the `AlienVault` API engine with `Anubis` API to eliminate frequent `HTTP 429: Too Many Requests` errors and significantly improve scan reliability.

## [0.2.0] - 2026-03-18

### Added
- **Deep Scan Engine (`--deep`)**: Added Wayback Machine (Archive.org) integration for exhaustive historical subdomain discovery.
- **Technology Fingerprinting**: The status checker now extracts and displays `Server` and `X-Powered-By` headers using a lightweight `HEAD` request.
- **Treasure Highlighter**: Added visual tagging `[ INTERESTING ]` for high-value targets containing keywords like *admin, dev, staging, api, config*.
- **JSON Export (`--json`)**: Added support to export scan results into a structured JSON format.
- **Custom Timeout (`--timeout`)**: Allow users to define custom wait times for API requests.
- **Auto-Retry Mechanism**: Engines will now automatically retry up to 3 times before failing when encountering unstable APIs (like crt.sh or AlienVault).

### Changed
- Replaced the failing Wayback Machine default scan with AlienVault OTX (Passive DNS) for the default fast scan mode.
- Optimized `run_base_scan` logic to handle dynamic engine loading based on user arguments.

## [0.1.0] - 2026-03-18

### Added
- Initial release of Link-Compass reconnaissance tool.
- Passive subdomain enumeration engine using `crt.sh` (Certificate Transparency logs).
- Multi-threaded DNS resolution for identifying active subdomains.
- Concurrent HTTP/HTTPS status code prober (200, 403, 404, etc.) using native `urllib`.
- Modular architecture with dedicated directories for `/core`, `/modules`, and `/utils`.
- Support for automated result reporting and file exporting (`-o` flag).
- Global execution support for Linux, macOS, and Termux environments.
- Comprehensive documentation including `README.md`, `SECURITY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`.

### Fixed
- Resolved an issue where unresolvable subdomains would cause the status prober to hang.
- Fixed terminal color bleeding by implementing a clean ANSI escape reset in the UI utility.

### Security
- Implemented a "Zero-Bloat" architecture to eliminate security risks associated with third-party library dependencies.

