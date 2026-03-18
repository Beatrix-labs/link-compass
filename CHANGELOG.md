# Changelog

All notable changes to **Link-Compass** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

