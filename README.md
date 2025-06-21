# NEA Waste Management Recycling Page Scraper

This Python scraper extracts FAQs, press releases, and relevant content from the National Environment Agency (NEA) waste management recycling page.

## Features

- **FAQs Extraction**: Automatically detects and extracts frequently asked questions
- **Press Releases**: Finds press releases and news items
- **Content Sections**: Extracts general content organized by headings
- **Relevant Links**: Identifies and extracts relevant links related to recycling and waste management
- **JSON Output**: Saves all scraped data in structured JSON format
- **Error Handling**: Robust error handling for network issues and parsing problems

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with:

```bash
python scripts/scrape.py
```

The scraper will:
1. Fetch the NEA recycling page
2. Extract FAQs, press releases, and content
3. Save the data to a timestamped JSON file
4. Display a summary of the scraped content

### Output

The scraper generates a JSON file with the following structure:

```json
{
  "url": "https://www.nea.gov.sg/our-services/waste-management/recycling",
  "scraped_at": "2024-01-01T12:00:00",
  "faqs": [
    {
      "question": "What can I recycle?",
      "answer": "You can recycle paper, plastic, glass...",
      "source": "content_section"
    }
  ],
  "press_releases": [
    {
      "title": "New Recycling Initiative",
      "url": "https://www.nea.gov.sg/news/press-release",
      "source": "news_link"
    }
  ],
  "content_sections": [
    {
      "heading": "Recycling Guidelines",
      "content": ["Content paragraphs..."],
      "type": "section"
    }
  ],
  "relevant_links": [
    {
      "text": "Recycling Guide",
      "url": "https://www.nea.gov.sg/recycling-guide",
      "type": "relevant_link"
    }
  ]
}
```

## Customization

### Modifying the Target URL

To scrape a different NEA page, modify the `target_url` in the `NEAScraper` class:

```python
self.target_url = "https://www.nea.gov.sg/your-target-page"
```

### Adding New Content Types

You can extend the scraper by adding new extraction methods to the `NEAScraper` class:

```python
def extract_new_content_type(self, soup):
    # Your extraction logic here
    return extracted_data
```

### Custom Output Format

Modify the `save_data` method to output in different formats (CSV, XML, etc.) or integrate with databases.

## Error Handling

The scraper includes comprehensive error handling for:
- Network connectivity issues
- Invalid URLs
- HTML parsing errors
- Missing content elements

## Legal and Ethical Considerations

- **Respect robots.txt**: Check the website's robots.txt file before scraping
- **Rate Limiting**: The scraper includes delays to avoid overwhelming the server
- **Terms of Service**: Ensure compliance with NEA's terms of service
- **Data Usage**: Use scraped data responsibly and in accordance with applicable laws

## Troubleshooting

### Common Issues

1. **Connection Errors**: Check your internet connection and the target URL
2. **No Content Found**: The page structure may have changed; check the selectors
3. **Permission Errors**: Ensure you have write permissions in the current directory

### Debug Mode

To see more detailed output, you can modify the scraper to include debug prints:

```python
# Add debug prints in extraction methods
print(f"Debug: Found {len(elements)} elements with selector {selector}")
```

## Dependencies

- **requests**: HTTP library for making web requests
- **beautifulsoup4**: HTML parsing library
- **lxml**: XML/HTML parser backend for BeautifulSoup

## License

This scraper is provided for educational and research purposes. Please ensure compliance with all applicable laws and website terms of service.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the scraper.
