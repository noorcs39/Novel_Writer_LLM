import requests
from bs4 import BeautifulSoup
import time
import json
import os
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Set

class SacredTextsScraper:
    def __init__(self, base_delay: float = 1.0):
        """
        Initialize the Sacred Texts scraper
        
        Args:
            base_delay: Base delay between requests in seconds
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_delay = base_delay
        self.scraped_urls: Set[str] = set()
        self.failed_urls: List[str] = []
        
    def get_page_content(self, url: str) -> BeautifulSoup:
        """
        Fetch and parse a webpage
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object of the parsed page
        """
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Add delay to be respectful
            time.sleep(self.base_delay)
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            self.failed_urls.append(url)
            return None
    
    def extract_text_content(self, soup: BeautifulSoup, url: str) -> Dict[str, str]:
        """
        Extract meaningful text content from a Sacred Texts page
        
        Args:
            soup: BeautifulSoup object of the page
            url: Original URL for reference
            
        Returns:
            Dictionary with extracted content
        """
        if not soup:
            return None
            
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # Try to find the main content area
        main_content = None
        
        # Look for common content containers
        content_selectors = [
            'main',
            '.content',
            '#content', 
            '.main-content',
            'article',
            '.text-content'
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # If no specific content area found, use body
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            return None
        
        # Extract title
        title = ""
        title_elem = soup.find('title')
        if title_elem:
            title = title_elem.get_text().strip()
        
        # Extract main text content
        text_content = main_content.get_text(separator='\n', strip=True)
        
        # Clean up the text
        text_content = re.sub(r'\n\s*\n', '\n\n', text_content)  # Normalize line breaks
        text_content = re.sub(r'[ \t]+', ' ', text_content)  # Normalize spaces
        
        # Filter out very short content (likely navigation or error pages)
        if len(text_content.strip()) < 100:
            return None
        
        return {
            'url': url,
            'title': title,
            'content': text_content.strip(),
            'word_count': len(text_content.split()),
            'char_count': len(text_content)
        }
    
    def find_linked_pages(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Find additional pages linked from index pages
        
        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL for resolving relative links
            
        Returns:
            List of URLs to scrape
        """
        if not soup:
            return []
        
        links = []
        base_domain = urlparse(base_url).netloc
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Skip external links, anchors, and common non-content links
            if (href.startswith('http') and base_domain not in href) or \
               href.startswith('#') or \
               href.startswith('mailto:') or \
               href.startswith('javascript:'):
                continue
            
            # Convert relative URLs to absolute
            full_url = urljoin(base_url, href)
            
            # Only include sacred-texts.com URLs
            if 'sacred-texts.com' in full_url:
                links.append(full_url)
        
        return list(set(links))  # Remove duplicates
    
    def scrape_url(self, url: str, max_depth: int = 2, current_depth: int = 0) -> List[Dict[str, str]]:
        """
        Scrape a URL and optionally follow links
        
        Args:
            url: URL to scrape
            max_depth: Maximum depth to follow links
            current_depth: Current recursion depth
            
        Returns:
            List of extracted content dictionaries
        """
        if url in self.scraped_urls or current_depth > max_depth:
            return []
        
        self.scraped_urls.add(url)
        results = []
        
        soup = self.get_page_content(url)
        if not soup:
            return results
        
        # Extract content from current page
        content = self.extract_text_content(soup, url)
        if content:
            results.append(content)
            print(f"Extracted content from {url} ({content['word_count']} words)")
        
        # If this is an index page and we haven't reached max depth, follow links
        if current_depth < max_depth and ('index.htm' in url or '/index.' in url):
            linked_pages = self.find_linked_pages(soup, url)
            print(f"Found {len(linked_pages)} linked pages from {url}")
            
            for linked_url in linked_pages[:20]:  # Limit to prevent overwhelming
                if linked_url not in self.scraped_urls:
                    sub_results = self.scrape_url(linked_url, max_depth, current_depth + 1)
                    results.extend(sub_results)
        
        return results
    
    def scrape_urls(self, urls: List[str], max_depth: int = 1) -> List[Dict[str, str]]:
        """
        Scrape multiple URLs
        
        Args:
            urls: List of URLs to scrape
            max_depth: Maximum depth to follow links
            
        Returns:
            List of all extracted content
        """
        all_content = []
        
        for i, url in enumerate(urls, 1):
            print(f"\nProcessing URL {i}/{len(urls)}: {url}")
            try:
                content = self.scrape_url(url, max_depth)
                all_content.extend(content)
                print(f"Extracted {len(content)} pieces of content from {url}")
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                self.failed_urls.append(url)
        
        return all_content
    
    def save_content(self, content_list: List[Dict[str, str]], output_dir: str = "scraped_data"):
        """
        Save scraped content to files
        
        Args:
            content_list: List of content dictionaries
            output_dir: Directory to save files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as JSON
        json_path = os.path.join(output_dir, "sacred_texts_content.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(content_list, f, indent=2, ensure_ascii=False)
        
        # Save as plain text for training
        txt_path = os.path.join(output_dir, "sacred_texts_training.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            for item in content_list:
                f.write(f"Title: {item['title']}\n")
                f.write(f"URL: {item['url']}\n")
                f.write("=" * 50 + "\n")
                f.write(item['content'])
                f.write("\n" + "=" * 50 + "\n\n")
        
        # Save statistics
        stats = {
            'total_documents': len(content_list),
            'total_words': sum(item['word_count'] for item in content_list),
            'total_characters': sum(item['char_count'] for item in content_list),
            'failed_urls': self.failed_urls,
            'scraped_urls_count': len(self.scraped_urls)
        }
        
        stats_path = os.path.join(output_dir, "scraping_stats.json")
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        print(f"\nScraping completed!")
        print(f"Total documents: {stats['total_documents']}")
        print(f"Total words: {stats['total_words']:,}")
        print(f"Total characters: {stats['total_characters']:,}")
        print(f"Failed URLs: {len(stats['failed_urls'])}")
        print(f"Content saved to: {output_dir}")

def main():
    # URLs to scrape
    urls = [
        "https://www.sacred-texts.com/afr/index.htm",
        "https://www.sacred-texts.com/aor/dv/index.htm",
        "https://www.sacred-texts.com/aor/twain/letearth.htm",
        "https://www.sacred-texts.com/aor/einstein/einprayr.htm",
        "https://www.sacred-texts.com/aor/einstein/einsci.htm",
        "https://www.sacred-texts.com/aor/einstein/einbucky.htm",
        "https://www.sacred-texts.com/alc/index.htm",
        "https://www.sacred-texts.com/ame/pow/index.htm",
        "https://www.sacred-texts.com/ame/fpg/index.htm",
        "https://www.sacred-texts.com/ame/cig/index.htm",
        "https://www.sacred-texts.com/ane/index.htm",
        "https://www.sacred-texts.com/astro/index.htm",
        "https://www.sacred-texts.com/asia/index.htm",
        "https://www.sacred-texts.com/cla/plato/timaeus.htm",
        "https://www.sacred-texts.com/cla/plato/critias.htm",
        "https://www.sacred-texts.com/aus/index.htm",
        "https://www.sacred-texts.com/neu/basque/index.htm",
        "https://www.sacred-texts.com/bhi/index.htm",
        "https://www.sacred-texts.com/bib/index.htm",
        "https://www.sacred-texts.com/bud/index.htm",
        "https://www.sacred-texts.com/neu/celt/index.htm",
        "https://www.sacred-texts.com/chr/index.htm",
        "https://www.sacred-texts.com/cla/index.htm",
        "https://www.sacred-texts.com/comp/index.htm"
    ]
    
    # Initialize scraper
    scraper = SacredTextsScraper(base_delay=1.5)  # Be respectful with delays
    
    # Scrape content
    print("Starting Sacred Texts scraping...")
    content = scraper.scrape_urls(urls, max_depth=1)  # Adjust depth as needed
    
    # Save results
    scraper.save_content(content)

if __name__ == "__main__":
    main()