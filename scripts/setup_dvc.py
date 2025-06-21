#!/usr/bin/env python3
"""
Setup DVC for Data Versioning
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Setup DVC for data versioning"""
    print("🚀 Setting up DVC for Data Versioning")
    print("=" * 50)
    
    # Check if DVC is installed
    if not run_command("dvc --version", "Checking DVC installation"):
        print("❌ DVC is not installed. Please install it first:")
        print("   pip install dvc")
        return False
    
    # Initialize DVC
    if not run_command("dvc init", "Initializing DVC"):
        return False
    
    # Add .dvc to .gitignore if not already there
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if ".dvc/cache" not in content:
            with open(gitignore_path, "a", encoding="utf-8") as f:
                f.write("\n# DVC cache\n.dvc/cache\n")
            print("✅ Added .dvc/cache to .gitignore")
    else:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write("# DVC cache\n.dvc/cache\n")
        print("✅ Created .gitignore with DVC cache exclusion")
    
    # Add raw data directory to DVC
    raw_data_path = Path("data/raw")
    if raw_data_path.exists():
        if not run_command(f"dvc add {raw_data_path}", f"Adding {raw_data_path} to DVC"):
            return False
        
        # Check if .dvc file was created
        dvc_file = raw_data_path.with_suffix('.dvc')
        if dvc_file.exists():
            print(f"✅ DVC file created: {dvc_file}")
        else:
            print(f"❌ DVC file not created for {raw_data_path}")
            return False
    else:
        print(f"⚠️  Raw data directory not found: {raw_data_path}")
        print("   Please run the scraper first to generate data")
        return False
    
    # Add .dvc files to git
    if not run_command("git add .dvc .gitignore", "Adding DVC files to git"):
        return False
    
    # Commit the changes
    if not run_command('git commit -m "Add raw docs with DVC"', "Committing DVC setup"):
        return False
    
    print("\n🎉 DVC Setup Complete!")
    print("=" * 50)
    print("📁 Data is now versioned with DVC")
    print("💾 Local cache location: .dvc/cache")
    print("📋 Next steps:")
    print("   1. Check DVC status: dvc status")
    print("   2. View tracked files: dvc list .")
    print("   3. Update data: dvc add data/raw && git add data/raw.dvc && git commit -m 'Update data'")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 