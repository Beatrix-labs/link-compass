# Contributing to Link-Compass

First, thank you for considering contributing to Link-Compass. The open-source community is what makes tools like this powerful, and Beatrix Labs welcomes developers, bug hunters, and security enthusiasts to help improve this project.

The following is a set of guidelines for contributing to Link-Compass. These are mostly guidelines, not hard rules, but adhering to them helps us review and merge your pull requests significantly faster.

## Core Philosophy: The Zero-Bloat Rule

Before you write any code, please understand the core architectural philosophy of Link-Compass: **Zero-Bloat**. 

This tool is designed to run natively on any system (Linux, macOS, Windows, Termux) without requiring the user to run `pip install`. 
- **Rule 1:** You must only use Python Standard Libraries (e.g., `urllib`, `socket`, `concurrent.futures`, `json`, `sys`, `os`). 
- **Rule 2:** Do not introduce third-party dependencies like `requests`, `colorama`, or `beautifulsoup4`. Any pull request introducing an external dependency will be rejected.

## How Can You Contribute?

### 1. Reporting Bugs
If you find a bug, please check the existing issues to ensure it has not already been reported. If it is a new bug, open an issue and include:
- Your operating system and Python version.
- The exact command you ran.
- The expected behavior versus the actual behavior.
- A full traceback of the error (if applicable).

*Note: If you find a security vulnerability, do not open a public issue. Please refer to our `SECURITY.md` file.*

### 2. Suggesting Enhancements
We are always looking for ways to make Link-Compass faster and more accurate. When suggesting a feature:
- Explain why this enhancement would be useful to Bug Bounty hunters or security researchers.
- Provide a potential use case.
- Keep in mind that features must align with the lightweight, passive reconnaissance nature of the tool.

### 3. Submitting Pull Requests
If you want to contribute code, follow this workflow:

1. **Fork the repository** and clone it to your local machine.
2. **Create a new branch** for your feature or bug fix:
   `git checkout -b feature/your-feature-name` or `git checkout -b fix/issue-description`
3. **Write your code** ensuring it adheres to the Zero-Bloat rule and matches the existing coding style.
4. **Test your code** extensively. Ensure that the multithreading engine remains stable and memory leaks are avoided.
5. **Commit your changes** using clear and descriptive commit messages.
6. **Push to your fork** and submit a Pull Request to the `main` branch of the Beatrix Labs repository.

## Coding Standards

To maintain a clean and readable codebase, please adhere to the following standards:
- Use PEP 8 compliance for Python code.
- Maintain the modular directory structure (`/core`, `/modules`, `/utils`). Do not put everything in the main file.
- Keep CLI output clean, aligned, and professional. Use the native ANSI escape codes provided in `config.py` for terminal coloring. Do not use emojis in the terminal output.
- Write clear comments for complex logic, especially within the multithreading or network request blocks.

## Commit Message Guidelines

We prefer structured commit messages to keep the project history clean and understandable:
- `feat:` for new features (e.g., `feat: add DNS wildcard filtering`)
- `fix:` for bug fixes (e.g., `fix: resolve timeout exception in status checker`)
- `docs:` for documentation updates (e.g., `docs: update README installation guide`)
- `refactor:` for code changes that neither fix a bug nor add a feature

Thank you for dedicating your time to making Link-Compass better.

Beatrix Labs
