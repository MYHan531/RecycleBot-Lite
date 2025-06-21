#!/usr/bin/env python3
"""
NEA Waste Management Recycling Page Scraper
Scrapes FAQs and press releases from NEA's recycling page
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os
from urllib.parse import urljoin, urlparse
import re

class NEAScraper:
    def __init__(self):
        self.base_url = "https://www.nea.gov.sg"
        self.target_url = "https://www.nea.gov.sg/our-services/waste-management/recycling"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page_content(self, url):
        """Fetch page content with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_faqs(self, soup):
        """Extract FAQs from the page"""
        faqs = []
        
        # Look for common FAQ patterns
        faq_selectors = [
            '.faq-item',
            '.faq',
            '[class*="faq"]',
            '[class*="accordion"]',
            '.question',
            '.answer'
        ]
        
        for selector in faq_selectors:
            faq_elements = soup.select(selector)
            if faq_elements:
                print(f"Found {len(faq_elements)} FAQ elements with selector: {selector}")
                break
        
        # If no specific FAQ elements found, look for content that might be FAQs
        if not faq_elements:
            # Look for content with question-like patterns
            content_sections = soup.find_all(['div', 'section'], class_=re.compile(r'(content|text|body)', re.I))
            for section in content_sections:
                # Look for question-answer patterns
                questions = section.find_all(['h3', 'h4', 'h5', 'strong'], string=re.compile(r'\?$'))
                for q in questions:
                    answer = q.find_next_sibling(['p', 'div'])
                    if answer:
                        faqs.append({
                            'question': q.get_text(strip=True),
                            'answer': answer.get_text(strip=True),
                            'source': 'content_section'
                        })
        
        return faqs
    
    def extract_press_releases(self, soup):
        """Extract press releases and news items"""
        press_releases = []
        
        # Look for press release patterns
        pr_selectors = [
            '.press-release',
            '.news-item',
            '.article',
            '[class*="press"]',
            '[class*="news"]',
            '.media-release'
        ]
        
        for selector in pr_selectors:
            pr_elements = soup.select(selector)
            if pr_elements:
                print(f"Found {len(pr_elements)} press release elements with selector: {selector}")
                break
        
        # If no specific press release elements, look for news-like content
        if not pr_elements:
            # Look for links that might be press releases
            news_links = soup.find_all('a', href=re.compile(r'(press|news|media|release)', re.I))
            for link in news_links:
                title = link.get_text(strip=True)
                href = link.get('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    press_releases.append({
                        'title': title,
                        'url': full_url,
                        'source': 'news_link'
                    })
        
        return press_releases
    
    def extract_general_content(self, soup):
        """Extract general content sections"""
        content = []
        
        # Extract main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'(content|main|body)', re.I))
        
        if main_content:
            # Extract headings and their content
            headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for heading in headings:
                section_content = []
                next_elem = heading.find_next_sibling()
                
                # Collect content until next heading
                while next_elem and next_elem.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    if next_elem.name in ['p', 'div', 'ul', 'ol']:
                        text = next_elem.get_text(strip=True)
                        if text:
                            section_content.append(text)
                    next_elem = next_elem.find_next_sibling()
                
                if section_content:
                    content.append({
                        'heading': heading.get_text(strip=True),
                        'content': section_content,
                        'type': 'section'
                    })
        
        return content
    
    def extract_links(self, soup):
        """Extract relevant links from the page"""
        links = []
        
        # Find all links
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href')
            text = link.get_text(strip=True)
            
            if href and text:
                # Filter for relevant links
                relevant_keywords = ['recycling', 'waste', 'environment', 'sustainability', 'green']
                if any(keyword in text.lower() or keyword in href.lower() for keyword in relevant_keywords):
                    full_url = urljoin(self.base_url, href)
                    links.append({
                        'text': text,
                        'url': full_url,
                        'type': 'relevant_link'
                    })
        
        return links
    
    def scrape_page(self):
        """Main scraping function"""
        print(f"Scraping: {self.target_url}")
        
        # Get page content
        html_content = self.get_page_content(self.target_url)
        if not html_content:
            return None
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract different types of content
        scraped_data = {
            'url': self.target_url,
            'scraped_at': datetime.now().isoformat(),
            'faqs': self.extract_faqs(soup),
            'press_releases': self.extract_press_releases(soup),
            'content_sections': self.extract_general_content(soup),
            'relevant_links': self.extract_links(soup)
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
        
        print("="*50)

def main():
    """Main function"""
    scraper = NEAScraper()
    
    print("Starting NEA Waste Management Recycling Page Scraper...")
    
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