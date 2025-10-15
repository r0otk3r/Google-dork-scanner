# Google Dork Scanner

This document contains the full Python script and usage instructions for a simple Google Dork scanner that uses the Google Custom Search API. It saves found links to a text file (one link per line).

> **Warning:** respect Google's Terms of Service. Abuse of Google APIs or automated scraping of web properties can result in account suspension.

---

## Prerequisites

* Python 3.8+.
* `requests` library (`pip install requests`).
* A Google Cloud API key with the Custom Search API enabled and a Custom Search Engine (CSE) ID (cx).

---

## Installation

1. Create a Python virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

2. Save the script below to a file (e.g. `google_dork_scanner.py`).

3. Prepare a `dorks.txt` file with one Google Dork per line (comments allowed using `#`).

4. (Optional) Prepare an `exclude_domains.txt` file with one domain per line to filter false positives.

---

## Usage

```bash
python3 google_dork_scanner.py --dorks dorks.txt --output dork_results.txt --max-results 50 --exclude exclude_domains.txt
```

### Arguments

* `--dorks`: Path to the file containing Google Dork queries (required).
* `--output`: Output file to save results (default: `dork_results.txt`).
* `--max-results`: Maximum results per query (default: 50).
* `--exclude`: Path to a file containing domains to exclude (one per line).

---

## Notes & Security

* The script rotates through `API_KEYS` to avoid single-key rate limits. Be mindful of quotas and billing on your Google Cloud project.
* Use this tool responsibly and only against targets you are authorized to test.

---

## License

Use and modify at your own risk. No warranty.

---

## Official Channels

- [Telegram @r0otk3r](https://t.me/r0otk3r)
- [X @r0otk3r](https://x.com/r0otk3r)
