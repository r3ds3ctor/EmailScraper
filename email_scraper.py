import requests
from bs4 import BeautifulSoup
import re
import random
import argparse
from tqdm import tqdm
from colorama import Fore, Style, init
import logging
import time
import signal
import sys

# Initialize colorama for colored output
init(autoreset=True)

# Regular expression pattern for emails
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Set to store unique emails and links
found_emails = set()
found_links = set()

# List of user agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
]

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def signal_handler(sig, frame):
    """Handle Ctrl+C to safely exit and save results."""
    print(Fore.YELLOW + "\n[INFO] Process interrupted. Saving results...")
    save_results()
    print_summary()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def extract_emails(text):
    """Extract emails from the given text."""
    return re.findall(EMAIL_REGEX, text)

def get_page_content(url):
    """Fetch page content from the URL and ensure it's valid HTML."""
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        content_type = response.headers.get('Content-Type', '')
        if "text/html" not in content_type:
            return None
        
        if response.status_code == 200:
            return response.text  
    except requests.exceptions.RequestException:
        pass  
    return None

def extract_links_and_emails(url, page_content):
    """Extract links and emails from the given page content and add them to sets."""
    try:
        soup = BeautifulSoup(page_content, 'html.parser')  
    except Exception:
        return set()
    
    links = set()
    emails = extract_emails(page_content)
    found_emails.update(emails)
    
    for link in soup.find_all('a', href=True):
        full_link = link['href']
        if full_link.startswith('http'):
            links.add(full_link)
    found_links.update(links)
    
    return links

def crawl_links(urls, max_depth):
    """Recursively crawl links and extract emails up to a specified depth."""
    for depth in range(1, max_depth + 1):
        new_links = set()
        progress_bar = tqdm(total=len(urls), desc=f"{Fore.GREEN}Crawling Depth {depth}/{max_depth}", bar_format='{l_bar}{bar} {n_fmt}/{total_fmt}', leave=True, dynamic_ncols=True)
        for url in urls:
            page_content = get_page_content(url)
            if page_content:
                new_links.update(extract_links_and_emails(url, page_content))
            progress_bar.update(1)
        progress_bar.close()
        save_results()
        if not new_links:
            break
        urls = new_links

def save_results():
    """Save all found links and emails to their respective files."""
    with open("links.txt", "w") as file:
        for link in found_links:
            file.write(link + "\n")
    
    with open("EmailExtracted.txt", "w") as file:
        for email in found_emails:
            file.write(email + "\n")

def print_summary():
    """Prints the final summary of extracted links and emails."""
    print(Fore.CYAN + "\n================ SUMMARY ================")
    print(Fore.GREEN + f"Total Links Found: {len(found_links)}")
    print(Fore.GREEN + f"Total Emails Extracted: {len(found_emails)}")
    print(Fore.CYAN + "========================================\n")

def main():
    """Main function to get user input and start scraping."""
    parser = argparse.ArgumentParser(description="Email Scraper v2")
    parser.add_argument("-r", "--recursion", type=int, default=1, help="Recursion depth (default: 1)")
    args = parser.parse_args()

    print(Fore.CYAN + "=== Email Scraper v2 ===")
    url = input(Fore.CYAN + "Enter the URL to scrape (e.g., https://example.com): ")
    
    if not url.startswith("http"):
        print(Fore.RED + "[ERROR] Please enter a valid URL starting with http:// or https://")
        return
    
    print(Fore.GREEN + "\nStarting to scrape the main page...")
    crawl_links({url}, args.recursion)
    save_results()
    print_summary()

if __name__ == "__main__":
    main()
