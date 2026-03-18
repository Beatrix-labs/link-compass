# Security Policy

**Beatrix Labs** takes the security of our open-source projects seriously. We appreciate the efforts of the security community and Bug Bounty hunters in making our tools safer and more reliable.

This document outlines our security policy, including which versions are currently supported and the protocol for reporting a vulnerability.

## Supported Versions

We currently provide security updates and patches only for the major versions listed below. If you are using an older version, we strongly recommend updating to the latest stable release.

| Version | Supported          |
| :---    | :---               |
| > 0.1.x | Yes                |
| < 0.1.x | No                 |

*Note: As Link-Compass is in its early development stages (v0.1.x), all minor updates within this branch will receive immediate security patches.*

## Reporting a Vulnerability

If you discover a security vulnerability within Link-Compass or any of its modules, please follow this coordinated disclosure process.

**Do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.**

Instead, please report it privately by sending an email directly to the project maintainers:
* **Email:** sushilibdev@gmail.com
* **Subject Line:** [Vulnerability Report] Link-Compass - <Brief Description>

### What to Include in Your Report

To help us triage and resolve the issue quickly, please include the following information in your email:
1. **Description:** A detailed summary of the vulnerability.
2. **Steps to Reproduce:** Exact steps, commands, or environmental setups required to replicate the issue.
3. **Impact:** The potential security impact if the vulnerability is exploited (e.g., Remote Code Execution, Denial of Service, Information Disclosure).
4. **Proof of Concept (PoC):** Any scripts, logs, or screenshots demonstrating the exploit.
5. **Proposed Mitigation:** (Optional) If you have a fix or suggestion on how to patch the vulnerability.

## Response Timeline

We are committed to resolving security issues promptly. You can expect the following timeline:
- **Acknowledgment:** We will acknowledge receipt of your vulnerability report within 48 hours.
- **Triage & Validation:** We will confirm the vulnerability and determine its severity within 5 business days.
- **Patch Development:** A patch will be developed and tested.
- **Disclosure:** Once the vulnerability has been patched and released, we will publicly acknowledge your contribution in our release notes and security advisories (unless you prefer to remain anonymous).

## Out of Scope

The following issues are generally considered out of scope and do not pose a direct security threat to the tool's architecture:
- Issues related to third-party APIs (e.g., crt.sh) going offline or responding with errors.
- Lack of rate-limiting on the target's end (as Link-Compass is a client-side testing tool).
- Vulnerabilities that require full access to the user's local machine or Termux environment to exploit.

Thank you for helping keep the Beatrix Labs ecosystem secure.
