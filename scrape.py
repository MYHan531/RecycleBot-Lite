#!/usr/bin/env python3
"""
NEA Waste Statistics and Overall Recycling Page Scraper
Scrapes waste statistics, recycling data, and trends from NEA's waste statistics page using Trafilatura
"""

import requests
from bs4 import BeautifulSoup
import trafilatura
import json
import time
from datetime import datetime
import os
from urllib.parse import urljoin, urlparse
import re

class NEAScraper:
    def __init__(self):
        self.base_url = "https://www.nea.gov.sg"
        self.target_url = "https://www.nea.gov.sg/our-services/waste-management/waste-statistics-and-overall-recycling"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Create data/raw directory if it doesn't exist
        self.data_dir = "data/raw"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def get_page_content(self, url):
        """Fetch page content with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_content_with_trafilatura(self, html_content, url):
        """Extract clean content using Trafilatura"""
        try:
            # Extract main content
            extracted_text = trafilatura.extract(html_content, url=url, output_format='text')
            extracted_markdown = trafilatura.extract(html_content, url=url, output_format='markdown')
            extracted_json = trafilatura.extract(html_content, url=url, output_format='json')
            
            # Parse JSON to get metadata
            metadata = {}
            if extracted_json:
                try:
                    metadata = json.loads(extracted_json)
                except:
                    pass
            
            return {
                'text': extracted_text,
                'markdown': extracted_markdown,
                'metadata': metadata
            }
        except Exception as e:
            print(f"Error extracting content with Trafilatura: {e}")
            return None
    
    def extract_statistics_tables(self, soup):
        """Extract statistics tables from the waste statistics page"""
        tables = []
        
        # Find all tables on the page
        table_elements = soup.find_all('table')
        
        for i, table in enumerate(table_elements):
            table_data = {
                'table_index': i,
                'headers': [],
                'rows': [],
                'title': ''
            }
            
            # Try to find table title (look for preceding heading or caption)
            prev_elem = table.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'caption'])
            if prev_elem:
                table_data['title'] = prev_elem.get_text(strip=True)
            
            # Extract headers
            header_row = table.find('tr')
            if header_row:
                headers = header_row.find_all(['th', 'td'])
                table_data['headers'] = [h.get_text(strip=True) for h in headers]
                
                # Extract data rows
                data_rows = table.find_all('tr')[1:]  # Skip header row
                for row in data_rows:
                    cells = row.find_all(['td', 'th'])
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    if row_data:  # Only add non-empty rows
                        table_data['rows'].append(row_data)
            
            if table_data['rows']:  # Only add tables with data
                tables.append(table_data)
        
        return tables
    
    def extract_key_statistics(self, soup, trafilatura_content):
        """Extract key statistics and highlights from the page"""
        statistics = {
            'key_highlights': [],
            'waste_trends': [],
            'recycling_rates': [],
            'annual_data': {}
        }
        
        # Extract key highlights from text content
        if trafilatura_content and trafilatura_content.get('text'):
            text_content = trafilatura_content['text']
            
            # Look for key statistics patterns
            # Daily domestic waste per capita
            domestic_pattern = r'(\d+\.?\d*)\s*kg.*per capita.*(\d{4})'
            domestic_matches = re.findall(domestic_pattern, text_content, re.IGNORECASE)
            for match in domestic_matches:
                statistics['waste_trends'].append({
                    'metric': 'Daily domestic waste per capita',
                    'value': match[0],
                    'unit': 'kg',
                    'year': match[1]
                })
            
            # Overall recycling rate
            recycling_pattern = r'(\d+)\s*per cent.*recycling.*(\d{4})'
            recycling_matches = re.findall(recycling_pattern, text_content, re.IGNORECASE)
            for match in recycling_matches:
                statistics['recycling_rates'].append({
                    'metric': 'Overall recycling rate',
                    'value': match[0],
                    'unit': 'percent',
                    'year': match[1]
                })
            
            # Household recycling participation
            household_pattern = r'(\d+)\s*per cent.*household.*recycle.*(\d{4})'
            household_matches = re.findall(household_pattern, text_content, re.IGNORECASE)
            for match in household_matches:
                statistics['key_highlights'].append({
                    'metric': 'Household recycling participation',
                    'value': match[0],
                    'unit': 'percent',
                    'year': match[1]
                })
        
        return statistics
    
    def extract_annual_data(self, soup):
        """Extract annual waste and recycling data"""
        annual_data = {}
        
        # Look for specific data patterns in tables
        tables = soup.find_all('table')
        for table in tables:
            # Look for year-based data
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    first_cell = cells[0].get_text(strip=True)
                    # Check if first cell contains a year
                    year_match = re.search(r'(\d{4})', first_cell)
                    if year_match:
                        year = year_match.group(1)
                        if year not in annual_data:
                            annual_data[year] = {}
                        
                        # Extract data from other cells
                        for i, cell in enumerate(cells[1:], 1):
                            cell_text = cell.get_text(strip=True)
                            if cell_text and cell_text != '':
                                # Try to identify the data type
                                if '%' in cell_text:
                                    annual_data[year][f'rate_{i}'] = cell_text
                                elif re.search(r'\d+', cell_text):
                                    annual_data[year][f'value_{i}'] = cell_text
        
        return annual_data
    
    def extract_content_sections(self, soup, trafilatura_content):
        """Extract content sections using Trafilatura and BeautifulSoup"""
        content = []
        
        # Method 1: Use Trafilatura content
        if trafilatura_content:
            if trafilatura_content.get('text'):
                content.append({
                    'heading': 'Main Content (Trafilatura)',
                    'content': trafilatura_content['text'].split('\n'),
                    'type': 'trafilatura_text'
                })
            
            if trafilatura_content.get('markdown'):
                content.append({
                    'heading': 'Main Content (Markdown)',
                    'content': trafilatura_content['markdown'].split('\n'),
                    'type': 'trafilatura_markdown'
                })
        
        # Method 2: Use BeautifulSoup to extract structured content
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
                        'type': 'beautifulsoup_section'
                    })
        
        return content
    
    def extract_relevant_links(self, soup):
        """Extract relevant links from the page"""
        links = []
        
        # Find all links
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href')
            text = link.get_text(strip=True)
            
            if href and text:
                # Filter for relevant links
                relevant_keywords = ['recycling', 'waste', 'environment', 'sustainability', 'green', 'statistics', 'report']
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
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract content with Trafilatura
        trafilatura_content = self.extract_content_with_trafilatura(html_content, self.target_url)
        
        # Extract different types of content
        scraped_data = {
            'url': self.target_url,
            'scraped_at': datetime.now().isoformat(),
            'page_title': 'Waste Statistics and Overall Recycling',
            'statistics_tables': self.extract_statistics_tables(soup),
            'key_statistics': self.extract_key_statistics(soup, trafilatura_content),
            'annual_data': self.extract_annual_data(soup),
            'content_sections': self.extract_content_sections(soup, trafilatura_content),
            'relevant_links': self.extract_relevant_links(soup),
            'trafilatura_metadata': trafilatura_content.get('metadata', {}) if trafilatura_content else {}
        }
        
        return scraped_data
    
    def save_data(self, data, filename=None):
        """Save scraped data to JSON file in data/raw folder with improved naming"""
        if not filename:
            # Use human-readable naming convention
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            filename = f"nea_waste_stats_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to: {filepath}")
        return filepath
    
    def print_summary(self, data):
        """Print a summary of scraped data"""
        print("\n" + "="*50)
        print("WASTE STATISTICS SCRAPING SUMMARY")
        print("="*50)
        print(f"URL: {data['url']}")
        print(f"Page Title: {data['page_title']}")
        print(f"Scraped at: {data['scraped_at']}")
        print(f"Statistics tables found: {len(data['statistics_tables'])}")
        print(f"Key statistics extracted: {len(data['key_statistics']['key_highlights'])} highlights")
        print(f"Annual data points: {len(data['annual_data'])} years")
        print(f"Content sections: {len(data['content_sections'])}")
        print(f"Relevant links: {len(data['relevant_links'])}")
        
        # Show Trafilatura metadata if available
        if data.get('trafilatura_metadata'):
            metadata = data['trafilatura_metadata']
            print(f"Trafilatura metadata: {len(metadata)} fields")
            if metadata.get('title'):
                print(f"  Title: {metadata['title']}")
            if metadata.get('author'):
                print(f"  Author: {metadata['author']}")
            if metadata.get('date'):
                print(f"  Date: {metadata['date']}")
        
        # Show key statistics
        if data['key_statistics']['key_highlights']:
            print("\nKey Highlights:")
            for i, highlight in enumerate(data['key_statistics']['key_highlights'][:3], 1):
                print(f"  {i}. {highlight['metric']}: {highlight['value']}{highlight['unit']} ({highlight['year']})")
        
        if data['key_statistics']['recycling_rates']:
            print("\nRecycling Rates:")
            for i, rate in enumerate(data['key_statistics']['recycling_rates'][:3], 1):
                print(f"  {i}. {rate['metric']}: {rate['value']}{rate['unit']} ({rate['year']})")
        
        if data['statistics_tables']:
            print("\nStatistics Tables:")
            for i, table in enumerate(data['statistics_tables'][:3], 1):
                print(f"  {i}. {table['title'] or f'Table {table['table_index']}'}: {len(table['rows'])} rows")
        
        print("="*50)     

def main():
    """Main function"""
    scraper = NEAScraper()
    
    print("Starting NEA Waste Statistics and Overall Recycling Page Scraper...")
    print("Using Trafilatura for enhanced content extraction")
    print("Focusing on waste statistics, recycling data, and trends")
    
    # Scrape the page
    data = scraper.scrape_page()
    
    if data:
        # Print summary
        scraper.print_summary(data)
        
        # Save data
        filename = scraper.save_data(data)
        
        print(f"\nScraping completed successfully!")
        print(f"Data saved to: {filename}")
        print(f"File naming convention: nea_waste_stats_YYYY-MM-DD_HHMMSS.json")
    else:
        print("Scraping failed. Please check the URL and try again.")

if __name__ == "__main__":
    main() 