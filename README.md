# EmailScraper v2

## Description
EmailScraper v2 is an enhanced Python tool designed to extract email addresses from websites while crawling internal links up to a specified depth. Unlike traditional scrapers, this tool dynamically follows internal links, collects new email addresses in real-time, and stores all extracted data in structured files. The script ensures stability, optimized crawling, and efficient progress tracking.

## Updates & Enhancements
Recursion Control: The user can specify the depth of crawling using -r X. If not specified, it defaults to 1 level.
<< Optimized Progress Bar: Now, only one progress bar is shown per recursion level, keeping output clean and readable.
<< Automatic Data Storage: Emails and links are progressively saved into EmailExtracted.txt and links.txt.
<< Background Execution & Stability: Crawling runs smoothly, avoiding crashes due to HTML parsing errors.
<< Graceful Exit with Ctrl+C: If interrupted, the script saves progress before exiting.
<< Content-Type Validation: Ensures only valid HTML pages are processed, preventing crashes on non-HTML responses.


## Features
- **Email Extraction**: Detects and extracts email addresses using a robust regular expression.
- **Progress Bar**: Displays real-time progress during the scraping process.
- **User-Agent Rotation**: Rotates user agents to minimize detection and blocking.
- **Lightweight & Easy to Use**: Simple execution with minimal dependencies.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/EmailScraper.git
   cd EmailScraper
   
2. Install dependencies:
   pip install -r requirements.txt

## Usage
Run the script and enter the target website URL: 
python3 email_scraper.py

## Example
Enter the URL to scrape (e.g., https://example.com): https://targetsite.com

## Output
<img width="736" alt="Screenshot 2025-02-28 at 7 34 09 AM" src="https://github.com/user-attachments/assets/08e23eec-d2fc-4d40-a996-880890422163" />


## Contributions
Contributions are welcome! If you have improvements or bug fixes, feel free to submit a pull request.

## Licence
This project is licensed under the MIT License.

Developed by [Alexander B]

## 🤝 Contributing
This project thrives on community contributions. If you'd like to suggest improvements, report issues, or add new features, feel free to open a pull request.  
If you’d like to support future development, you can do so here: 

☕ [buymeacoffee.com/alexboteroh]


