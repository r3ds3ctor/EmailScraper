import requests
from bs4 import BeautifulSoup
import re
import random
from tqdm import tqdm
from colorama import Fore, Style, init
import logging
import time

# Initialize colorama for colored output
init(autoreset=True)

# Regular expression pattern for emails
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Set to store unique emails
found_emails = set()

# List of user agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
]

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_emails(text):
    """Extract emails from the given text."""
    return re.findall(EMAIL_REGEX, text)

def get_page_content(url):
    """Fetch page content from the URL."""
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"Unable to access {url} (Status Code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
    return None

def scrape_emails(url):
    """Scrape emails from the given URL."""
    page_content = get_page_content(url)
    if not page_content:
        return

    # Display progress bar while processing
    for _ in tqdm(range(20), desc=Fore.GREEN + "Scraping Emails", bar_format='{l_bar}{bar} {n_fmt}/{total_fmt}'):
        time.sleep(0.05)
    
    emails = extract_emails(page_content)
    for email in emails:
        found_emails.add(email)

def main():
    """Main function to get user input and start scraping."""
    print(Fore.CYAN + "=== Email Scraper ===")
    url = input(Fore.CYAN + "Enter the URL to scrape (e.g., https://example.com): ")

    # Validate URL input
    if not url.startswith("http"):
        print(Fore.RED + "[ERROR] Please enter a valid URL starting with http:// or https://")
        return

    # Start scraping
    print(Fore.GREEN + "\nStarting to scrape...")
    scrape_emails(url)

    # Display the results
    print("\n" + "=" * 40)
    print(Fore.CYAN + "[SUMMARY OF FOUND EMAILS]")
    
    if found_emails:
        print(Fore.GREEN + "\nEmails:")
        for email in found_emails:
            print(f" - {email}")
    else:
        print(Fore.RED + "\nNo emails found.")

if __name__ == "__main__":
    main()
