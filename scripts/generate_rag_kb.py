#!/usr/bin/env python3
"""
Generate RAG Knowledge Base from NEA Scraped Data
Converts scraped JSON data into markdown snippets for RAG system
"""

import json
import os
import glob
from datetime import datetime
import re

class RAGKnowledgeBaseGenerator:
    def __init__(self):
        self.raw_data_dir = "data/raw"
        self.kb_output_dir = "data/knowledge_base"
        self.snippets_dir = os.path.join(self.kb_output_dir, "snippets")
        
        # Create directories
        os.makedirs(self.kb_output_dir, exist_ok=True)
        os.makedirs(self.snippets_dir, exist_ok=True)
    
    def load_latest_scraped_data(self):
        """Load the most recent scraped data file"""
        pattern = os.path.join(self.raw_data_dir, "nea_waste_stats_*.json")
        files = glob.glob(pattern)
        
        if not files:
            print("No scraped data files found!")
            return None
        
        # Get the most recent file
        latest_file = max(files, key=os.path.getctime)
        print(f"Loading latest data from: {latest_file}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_statistics_snippets(self, data):
        """Create markdown snippets from statistics data"""
        snippets = []
        
        # Key highlights snippet
        if data.get('key_statistics', {}).get('key_highlights'):
            highlights = data['key_statistics']['key_highlights']
            snippet = "# Key Waste Management Highlights\n\n"
            for highlight in highlights:
                snippet += f"- **{highlight['metric']}**: {highlight['value']}{highlight['unit']} ({highlight['year']})\n"
            snippet += f"\n*Source: NEA Waste Statistics Report*\n"
            snippets.append(("key_highlights", snippet))
        
        # Recycling rates snippet
        if data.get('key_statistics', {}).get('recycling_rates'):
            rates = data['key_statistics']['recycling_rates']
            snippet = "# Recycling Rate Trends\n\n"
            for rate in rates:
                snippet += f"- **{rate['metric']}**: {rate['value']}{rate['unit']} ({rate['year']})\n"
            snippet += f"\n*Source: NEA Waste Statistics Report*\n"
            snippets.append(("recycling_rates", snippet))
        
        # Waste trends snippet
        if data.get('key_statistics', {}).get('waste_trends'):
            trends = data['key_statistics']['waste_trends']
            snippet = "# Waste Generation Trends\n\n"
            for trend in trends:
                snippet += f"- **{trend['metric']}**: {trend['value']}{trend['unit']} ({trend['year']})\n"
            snippet += f"\n*Source: NEA Waste Statistics Report*\n"
            snippets.append(("waste_trends", snippet))
        
        return snippets
    
    def create_table_snippets(self, data):
        """Create markdown snippets from statistics tables"""
        snippets = []
        
        if not data.get('statistics_tables'):
            return snippets
        
        for i, table in enumerate(data['statistics_tables']):
            title = table.get('title', f'Table {i+1}')
            headers = table.get('headers', [])
            rows = table.get('rows', [])
            
            if not rows:
                continue
            
            snippet = f"# {title}\n\n"
            
            # Create markdown table
            if headers:
                snippet += "| " + " | ".join(headers) + " |\n"
                snippet += "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for row in rows:
                snippet += "| " + " | ".join(row) + " |\n"
            
            snippet += f"\n*Source: NEA Waste Statistics Report*\n"
            snippets.append((f"table_{i+1}_{title.lower().replace(' ', '_')}", snippet))
        
        return snippets
    
    def create_content_snippets(self, data):
        """Create markdown snippets from content sections"""
        snippets = []
        
        if not data.get('content_sections'):
            return snippets
        
        for i, section in enumerate(data['content_sections']):
            heading = section.get('heading', f'Section {i+1}')
            content = section.get('content', [])
            
            if not content:
                continue
            
            snippet = f"# {heading}\n\n"
            for paragraph in content:
                if paragraph.strip():
                    snippet += f"{paragraph}\n\n"
            
            snippet += f"*Source: NEA Waste Statistics Report*\n"
            snippets.append((f"content_{i+1}_{heading.lower().replace(' ', '_')}", snippet))
        
        return snippets
    
    def create_annual_data_snippets(self, data):
        """Create markdown snippets from annual data"""
        snippets = []
        
        if not data.get('annual_data'):
            return snippets
        
        annual_data = data['annual_data']
        
        # Group by year
        for year, year_data in annual_data.items():
            snippet = f"# Annual Waste Data - {year}\n\n"
            
            for key, value in year_data.items():
                if key.startswith('rate_'):
                    snippet += f"- **Recycling Rate**: {value}\n"
                elif key.startswith('value_'):
                    snippet += f"- **Waste Generated**: {value}\n"
                else:
                    snippet += f"- **{key.replace('_', ' ').title()}**: {value}\n"
            
            snippet += f"\n*Source: NEA Waste Statistics Report*\n"
            snippets.append((f"annual_data_{year}", snippet))
        
        return snippets
    
    def create_metadata_snippet(self, data):
        """Create metadata snippet"""
        metadata = data.get('trafilatura_metadata', {})
        url = data.get('url', '')
        scraped_at = data.get('scraped_at', '')
        
        snippet = "# Document Metadata\n\n"
        snippet += f"- **Source URL**: {url}\n"
        snippet += f"- **Scraped At**: {scraped_at}\n"
        
        if metadata.get('title'):
            snippet += f"- **Title**: {metadata['title']}\n"
        if metadata.get('author'):
            snippet += f"- **Author**: {metadata['author']}\n"
        if metadata.get('date'):
            snippet += f"- **Publication Date**: {metadata['date']}\n"
        if metadata.get('language'):
            snippet += f"- **Language**: {metadata['language']}\n"
        
        snippet += f"\n*Source: NEA Waste Statistics Report*\n"
        return [("metadata", snippet)]
    
    def generate_knowledge_base(self):
        """Generate the complete knowledge base"""
        print("Generating RAG Knowledge Base...")
        
        # Load scraped data
        data = self.load_latest_scraped_data()
        if not data:
            return
        
        all_snippets = []
        
        # Generate different types of snippets
        all_snippets.extend(self.create_metadata_snippet(data))
        all_snippets.extend(self.create_statistics_snippets(data))
        all_snippets.extend(self.create_table_snippets(data))
        all_snippets.extend(self.create_content_snippets(data))
        all_snippets.extend(self.create_annual_data_snippets(data))
        
        # Save individual snippets
        snippet_count = 0
        for snippet_id, content in all_snippets:
            filename = f"{snippet_id}.md"
            filepath = os.path.join(self.snippets_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            snippet_count += 1
            print(f"Created snippet: {filename}")
        
        # Create index file
        self.create_index_file(all_snippets)
        
        # Create combined knowledge base
        self.create_combined_kb(all_snippets)
        
        print(f"\nKnowledge base generated successfully!")
        print(f"Total snippets created: {snippet_count}")
        print(f"Output directory: {self.kb_output_dir}")
    
    def create_index_file(self, snippets):
        """Create an index file for all snippets"""
        index_content = "# NEA Waste Statistics Knowledge Base Index\n\n"
        index_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        index_content += "## Available Snippets\n\n"
        
        for snippet_id, content in snippets:
            # Extract title from content
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else snippet_id.replace('_', ' ').title()
            
            index_content += f"- **{snippet_id}**: {title}\n"
        
        index_path = os.path.join(self.kb_output_dir, "index.md")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
    
    def create_combined_kb(self, snippets):
        """Create a combined knowledge base file"""
        combined_content = "# NEA Waste Statistics - Complete Knowledge Base\n\n"
        combined_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        combined_content += "---\n\n"
        
        for snippet_id, content in snippets:
            combined_content += content + "\n\n---\n\n"
        
        combined_path = os.path.join(self.kb_output_dir, "complete_knowledge_base.md")
        with open(combined_path, 'w', encoding='utf-8') as f:
            f.write(combined_content)

def main():
    """Main function"""
    generator = RAGKnowledgeBaseGenerator()
    generator.generate_knowledge_base()

if __name__ == "__main__":
    main() 