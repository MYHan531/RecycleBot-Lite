#!/usr/bin/env python3
"""
NEA Waste Management Recycling Page Scraper (Simplified Version)
Uses only built-in Python libraries
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import re
from datetime import datetime
from html.parser import HTMLParser

class SimpleHTMLParser(HTMLParser):
    """Simple HTML parser to extract text content"""
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.current_tag = None
        self.current_attrs = {}
        self.links = []
        self.headings = []
        self.paragraphs = []
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        
        # Extract links
        if tag == 'a' and 'href' in self.current_attrs:
            self.links.append({
                'href': self.current_attrs['href'],
                'text': ''
            })
            
    def handle_endtag(self, tag):
        self.current_tag = None
        self.current_attrs = {}
        
    def handle_data(self, data):
        data = data.strip()
        if data:
            self.text_content.append(data)
            
            # Store headings
            if self.current_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                self.headings.append({
                    'level': self.current_tag,
                    'text': data
                })
            
            # Store paragraphs
            elif self.current_tag == 'p':
                self.paragraphs.append(data)
                
            # Store link text
            elif self.current_tag == 'a' and self.links:
                self.links[-1]['text'] = data

class SimpleNEAScraper:
    def __init__(self):
        self.base_url = "https://www.nea.gov.sg"
        # Try different possible URLs for recycling content
        self.possible_urls = [
            "https://www.nea.gov.sg/our-services/waste-management/recycling",
            "https://www.nea.gov.sg/our-services/waste-management",
            "https://www.nea.gov.sg/our-services",
            "https://www.nea.gov.sg"
        ]
        
    def get_page_content(self, url):
        """Fetch page content using urllib"""
        try:
            # Set up headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8')
                
        except urllib.error.URLError as e:
            print(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def find_recycling_page(self):
        """Find the correct recycling page URL"""
        for url in self.possible_urls:
            print(f"Trying URL: {url}")
            content = self.get_page_content(url)
            if content:
                print(f"Successfully accessed: {url}")
                return url, content
        return None, None
    
    def extract_content_sections(self, html_content):
        """Extract content sections from HTML"""
        parser = SimpleHTMLParser()
        parser.feed(html_content)
        
        content_sections = []
        
        # Group content by headings
        current_section = None
        for item in parser.text_content:
            # Check if this looks like a heading
            if re.match(r'^[A-Z][A-Za-z\s]+$', item) and len(item) < 100:
                if current_section:
                    content_sections.append(current_section)
                current_section = {
                    'heading': item,
                    'content': []
                }
            elif current_section:
                current_section['content'].append(item)
        
        if current_section:
            content_sections.append(current_section)
            
        return content_sections
    
    def extract_relevant_links(self, html_content):
        """Extract relevant links from HTML"""
        parser = SimpleHTMLParser()
        parser.feed(html_content)
        
        relevant_links = []
        relevant_keywords = ['recycling', 'waste', 'environment', 'sustainability', 'green']
        
        for link in parser.links:
            if link['text'] and link['href']:
                # Check if link is relevant
                if any(keyword in link['text'].lower() or keyword in link['href'].lower() 
                      for keyword in relevant_keywords):
                    full_url = urllib.parse.urljoin(self.base_url, link['href'])
                    relevant_links.append({
                        'text': link['text'],
                        'url': full_url,
                        'type': 'relevant_link'
                    })
        
        return relevant_links
    
    def extract_faqs(self, html_content):
        """Extract potential FAQs from content"""
        faqs = []
        
        # Look for question-answer patterns
        lines = html_content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            # Look for lines ending with question marks
            if line.endswith('?') and len(line) > 10:
                # Try to find an answer in the next few lines
                answer_lines = []
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not next_line.endswith('?'):
                        answer_lines.append(next_line)
                        if len(answer_lines) >= 2:  # Found a reasonable answer
                            break
                
                if answer_lines:
                    faqs.append({
                        'question': line,
                        'answer': ' '.join(answer_lines),
                        'source': 'text_analysis'
                    })
        
        return faqs
    
    def extract_press_releases(self, html_content):
        """Extract potential press releases and news items"""
        press_releases = []
        
        # Look for news-related content
        parser = SimpleHTMLParser()
        parser.feed(html_content)
        
        news_keywords = ['press', 'news', 'media', 'release', 'announcement']
        
        for link in parser.links:
            if link['text'] and link['href']:
                if any(keyword in link['text'].lower() or keyword in link['href'].lower() 
                      for keyword in news_keywords):
                    full_url = urllib.parse.urljoin(self.base_url, link['href'])
                    press_releases.append({
                        'title': link['text'],
                        'url': full_url,
                        'source': 'link_analysis'
                    })
        
        return press_releases
    
    def scrape_page(self):
        """Main scraping function"""
        print("Finding the correct NEA recycling page...")
        
        # Find the correct URL
        url, html_content = self.find_recycling_page()
        if not html_content:
            return None
        
        print(f"Scraping: {url}")
        
        # Extract different types of content
        scraped_data = {
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'faqs': self.extract_faqs(html_content),
            'press_releases': self.extract_press_releases(html_content),
            'content_sections': self.extract_content_sections(html_content),
            'relevant_links': self.extract_relevant_links(html_content)
        }
        
        return scraped_data
    
    def save_data(self, data, filename=None):
        """Save scraped data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nea_scraped_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to: {filename}")
        return filename
    
    def print_summary(self, data):
        """Print a summary of scraped data"""
        print("\n" + "="*50)
        print("SCRAPING SUMMARY")
        print("="*50)
        print(f"URL: {data['url']}")
        print(f"Scraped at: {data['scraped_at']}")
        print(f"FAQs found: {len(data['faqs'])}")
        print(f"Press releases found: {len(data['press_releases'])}")
        print(f"Content sections: {len(data['content_sections'])}")
        print(f"Relevant links: {len(data['relevant_links'])}")
        
        if data['faqs']:
            print("\nFAQs:")
            for i, faq in enumerate(data['faqs'][:3], 1):  # Show first 3
                print(f"  {i}. Q: {faq['question'][:100]}...")
                print(f"     A: {faq['answer'][:100]}...")
        
        if data['press_releases']:
            print("\nPress Releases:")
            for i, pr in enumerate(data['press_releases'][:3], 1):  # Show first 3
                print(f"  {i}. {pr['title'][:100]}...")
        
        if data['content_sections']:
            print("\nContent Sections:")
            for i, section in enumerate(data['content_sections'][:3], 1):  # Show first 3
                print(f"  {i}. {section['heading'][:100]}...")
        
        if data['relevant_links']:
            print("\nRelevant Links:")
            for i, link in enumerate(data['relevant_links'][:5], 1):  # Show first 5
                print(f"  {i}. {link['text'][:50]}... -> {link['url']}")
        
        print("="*50)

def main():
    """Main function"""
    scraper = SimpleNEAScraper()
    
    print("Starting NEA Waste Management Recycling Page Scraper (Simple Version)...")
    print("This version uses only built-in Python libraries.")
    
    # Scrape the page
    data = scraper.scrape_page()
    
    if data:
        # Print summary
        scraper.print_summary(data)
        
        # Save data
        filename = scraper.save_data(data)
        
        print(f"\nScraping completed successfully!")
        print(f"Data saved to: {filename}")
    else:
        print("Scraping failed. Please check the URL and try again.")

if __name__ == "__main__":
    main() 