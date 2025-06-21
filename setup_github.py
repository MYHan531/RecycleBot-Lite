#!/usr/bin/env python3
"""
Setup GitHub Repository Structure
Organizes files and prepares for GitHub commit
"""

import os
import shutil
import subprocess
from datetime import datetime

class GitHubSetup:
    def __init__(self):
        self.project_root = "."
        self.directories = [
            "data/raw",
            "data/knowledge_base/snippets",
            "docs"
        ]
    
    def create_directory_structure(self):
        """Create the required directory structure"""
        print("Creating directory structure...")
        
        for directory in self.directories:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created: {directory}")
    
    def check_file_structure(self):
        """Check if all required files are in place"""
        print("\nChecking file structure...")
        
        required_files = [
            "scrape.py",
            "generate_rag_kb.py",
            "convert_to_pdf.py",
            "requirements.txt",
            "README.md",
            "thinking_process.txt",
            "docs/service_blueprint.md"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
            else:
                print(f"✅ Found: {file_path}")
        
        if missing_files:
            print(f"\n❌ Missing files: {missing_files}")
            return False
        
        return True
    
    def generate_rag_knowledge_base(self):
        """Generate the RAG knowledge base from scraped data"""
        print("\nGenerating RAG Knowledge Base...")
        
        try:
            result = subprocess.run(['python', 'generate_rag_kb.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ RAG Knowledge Base generated successfully")
                return True
            else:
                print(f"❌ Error generating RAG KB: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error running RAG generation: {e}")
            return False
    
    def convert_blueprint_to_pdf(self):
        """Convert service blueprint to PDF"""
        print("\nConverting Service Blueprint to PDF...")
        
        try:
            result = subprocess.run(['python', 'convert_to_pdf.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ PDF conversion completed")
                return True
            else:
                print(f"⚠️  PDF conversion failed, but HTML version created")
                return False
                
        except Exception as e:
            print(f"❌ Error running PDF conversion: {e}")
            return False
    
    def create_gitignore(self):
        """Create .gitignore file"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp

# Data files (uncomment if you don't want to commit data)
# data/raw/*.json
# data/knowledge_base/

# Keep the directory structure but ignore content
data/raw/.gitkeep
data/knowledge_base/.gitkeep
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        
        print("✅ Created .gitignore file")
    
    def create_gitkeep_files(self):
        """Create .gitkeep files to preserve empty directories"""
        gitkeep_dirs = [
            "data/raw",
            "data/knowledge_base/snippets"
        ]
        
        for directory in gitkeep_dirs:
            gitkeep_file = os.path.join(directory, ".gitkeep")
            with open(gitkeep_file, 'w') as f:
                f.write("# This file ensures the directory is tracked by Git\n")
            print(f"✅ Created: {gitkeep_file}")
    
    def show_commit_instructions(self):
        """Show instructions for GitHub commit"""
        print("\n" + "="*60)
        print("GITHUB COMMIT INSTRUCTIONS")
        print("="*60)
        
        print("\n1. Initialize Git repository (if not already done):")
        print("   git init")
        
        print("\n2. Add all files to staging:")
        print("   git add .")
        
        print("\n3. Create initial commit:")
        print("   git commit -m \"Initial commit: NEA Waste Statistics Scraper and RAG Knowledge Base\"")
        
        print("\n4. Add remote repository (replace with your repo URL):")
        print("   git remote add origin https://github.com/yourusername/RecycleBot-Lite.git")
        
        print("\n5. Push to GitHub:")
        print("   git push -u origin main")
        
        print("\n" + "="*60)
        print("PROJECT STRUCTURE")
        print("="*60)
        
        self.print_project_structure()
    
    def print_project_structure(self):
        """Print the project structure"""
        structure = """
RecycleBot-Lite/
├── scrape.py                          # Main scraper script
├── generate_rag_kb.py                 # RAG knowledge base generator
├── convert_to_pdf.py                  # PDF conversion script
├── setup_github.py                    # This setup script
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
├── thinking_process.txt               # Development decision log
├── .gitignore                         # Git ignore rules
├── data/
│   ├── raw/                           # Scraped JSON data
│   │   ├── .gitkeep
│   │   └── nea_waste_stats_*.json     # Scraped data files
│   └── knowledge_base/                # RAG knowledge base
│       ├── snippets/                  # Individual markdown snippets
│       │   ├── .gitkeep
│       │   ├── metadata.md
│       │   ├── key_highlights.md
│       │   ├── recycling_rates.md
│       │   ├── waste_trends.md
│       │   ├── table_*.md
│       │   ├── content_*.md
│       │   └── annual_data_*.md
│       ├── index.md                   # Snippet index
│       └── complete_knowledge_base.md # Combined knowledge base
└── docs/
    ├── service_blueprint.md           # Service blueprint (markdown)
    ├── blueprint.pdf                  # Service blueprint (PDF)
    └── blueprint.html                 # Service blueprint (HTML fallback)
"""
        print(structure)
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Setting up GitHub repository structure...")
        
        # Create directory structure
        self.create_directory_structure()
        
        # Check file structure
        if not self.check_file_structure():
            print("\n❌ Some required files are missing. Please ensure all files are created.")
            return
        
        # Generate RAG knowledge base
        self.generate_rag_knowledge_base()
        
        # Convert blueprint to PDF
        self.convert_blueprint_to_pdf()
        
        # Create .gitignore
        self.create_gitignore()
        
        # Create .gitkeep files
        self.create_gitkeep_files()
        
        # Show commit instructions
        self.show_commit_instructions()
        
        print("\n🎉 Setup completed successfully!")
        print("📁 Your project is ready for GitHub commit.")

def main():
    """Main function"""
    setup = GitHubSetup()
    setup.run_setup()

if __name__ == "__main__":
    main() 