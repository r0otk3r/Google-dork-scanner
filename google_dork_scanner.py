#!/usr/bin/env python3
#By r0otk3r

import requests
import time
import argparse

# List of Google API Keys (rotate to bypass query limits)
API_KEYS = ["AIzaSyDSYmpwpwmf79fnkjsfa_yx3Y997547PkE", "AIzfkl8981asbf-OWzXvy4DdfdklkadacU4lB7pe-A"]
CX = "c29125701aqfkBRacd897492"  # Google Custom Search Engine ID

# Default domains to exclude (false positives)
DEFAULT_EXCLUDE_DOMAINS = ["bugs.mysql.com", "forum.glpi-project.org", "piwigo.org"]

def read_domains_from_file(file_path):
    """Read domains to exclude from a file."""
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            domains = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        return domains
    except FileNotFoundError:
        print(f"Warning: Exclude domains file '{file_path}' not found. Using default exclusions.")
        return DEFAULT_EXCLUDE_DOMAINS
    except Exception as e:
        print(f"Error reading exclude domains file: {e}. Using default exclusions.")
        return DEFAULT_EXCLUDE_DOMAINS

def google_dork(query, exclude_domains, max_results=100):
    results = []
    api_index = 0  # Start with first API key
    
    for start in range(1, min(max_results, 100) + 1, 10):  # Google API max 100 per query
        api_key = API_KEYS[api_index]
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={CX}&start={start}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    link = item['link']
                    
                    # Filter out false positives using provided exclude domains
                    if not any(domain in link for domain in exclude_domains):
                        results.append(link)  # Only store the link
            
            elif response.status_code == 403 or response.status_code == 429:
                print(f"API key {api_index + 1} quota exceeded or rate limited. Rotating...")
                api_index = (api_index + 1) % len(API_KEYS)
                if api_index == 0:
                    print("All API keys may be exhausted. Waiting 60 seconds...")
                    time.sleep(60)
                continue
                
            else:
                print(f"Error {response.status_code}: {response.text}")
                break
                
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break
            
        # Avoid rate limiting
        time.sleep(1)
        
        if len(results) >= max_results:
            break
    
    return results

def read_dorks_from_file(file_path):
    """Read Google Dork queries from a file."""
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            dorks = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        return dorks
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found")
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Google Dork Scanner")
    parser.add_argument(
        "--dorks",
        required=True,
        help="Path to a file containing Google Dork queries (one per line)"
    )
    parser.add_argument(
        "--output",
        default="dork_results.txt",
        help="Output file to save results (default: dork_results.txt)"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="Maximum results per query (default: 50)"
    )
    parser.add_argument(
        "--exclude",
        help="Path to a file containing domains to exclude (one per line)"
    )
    args = parser.parse_args()

    # Read Google Dork queries from the specified file
    try:
        dork_queries = read_dorks_from_file(args.dorks)
        if not dork_queries:
            print("No valid dorks found in the file.")
            return
    except FileNotFoundError as e:
        print(e)
        return

    # Read exclude domains from file or use defaults
    if args.exclude:
        exclude_domains = read_domains_from_file(args.exclude)
    else:
        exclude_domains = DEFAULT_EXCLUDE_DOMAINS

    print(f"Loaded {len(dork_queries)} dork queries")
    print(f"Using {len(API_KEYS)} API keys")
    print(f"Excluding {len(exclude_domains)} domains: {', '.join(exclude_domains)}")
    
    # Run multiple queries and save results
    all_results = []
    for i, query in enumerate(dork_queries, 1):
        print(f"[{i}/{len(dork_queries)}] Running query: {query}")
        results = google_dork(query, exclude_domains, max_results=args.max_results)
        all_results.extend(results)
        print(f"Found {len(results)} results for this query")

    # Save results to a file - only links, one per line
    try:
        with open(args.output, "w", encoding='utf-8') as f:
            # Write each link on a separate line
            for link in all_results:
                f.write(f"{link}\n")
                
        print(f"Successfully saved {len(all_results)} links to {args.output}")
        
    except Exception as e:
        print(f"Error saving results: {e}")

if __name__ == "__main__":
    main()
