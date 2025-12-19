#!/usr/bin/env python3

"""
Paper Structure Validator

Validates the document structure, section completeness, and consistency.
"""

import sys
from pathlib import Path
import yaml
import re

def validate_section_files(latex_dir):
    """Check that all referenced section files exist"""
    main_file = Path(latex_dir) / "main.tex"
    
    if not main_file.exists():
        return False, ["main.tex not found"]
    
    issues = []
    
    with open(main_file, 'r') as f:
        content = f.read()
    
    # Find all \input commands
    inputs = re.findall(r'\\input\{([^}]+)\}', content)
    
    for input_file in inputs:
        full_path = Path(latex_dir) / (input_file + ".tex")
        if not full_path.exists():
            issues.append(f"Referenced section file not found: {input_file}.tex")
    
    return len(issues) == 0, issues

def validate_metadata(metadata_file):
    """Check paper metadata"""
    issues = []
    
    if not Path(metadata_file).exists():
        return False, ["Metadata file not found"]
    
    try:
        with open(metadata_file, 'r') as f:
            data = yaml.safe_load(f)
        
        required_fields = ['title', 'scope', 'status']
        for field in required_fields:
            if field not in data:
                issues.append(f"Missing required metadata field: {field}")
        
        return len(issues) == 0, issues
    except Exception as e:
        return False, [f"Error reading metadata: {str(e)}"]

def check_section_status(status_file):
    """Check section drafting status"""
    if not Path(status_file).exists():
        return {}, []
    
    try:
        with open(status_file, 'r') as f:
            data = yaml.safe_load(f)
        return data.get('sections', {}), []
    except Exception as e:
        return {}, [f"Error reading section status: {str(e)}"]

def main():
    # Validate structure
    latex_dir = Path("latex")
    
    print("Paper Structure Validation")
    print("=" * 50)
    
    # Check section files
    print("\nChecking section files...")
    valid, issues = validate_section_files(latex_dir)
    if valid:
        print("✓ All section files present")
    else:
        for issue in issues:
            print(f"✗ {issue}")
    
    # Check metadata
    metadata_file = Path("open-agents/memory/paper-metadata.yaml")
    print("\nChecking metadata...")
    valid, issues = validate_metadata(metadata_file)
    if valid:
        print("✓ Metadata file valid")
    else:
        for issue in issues:
            print(f"✗ {issue}")
    
    # Check section status
    status_file = Path("open-agents/memory/section-status.yaml")
    print("\nChecking section completion status...")
    sections, issues = check_section_status(status_file)
    
    if sections:
        for section, data in sections.items():
            status = data.get('status', 'unknown')
            words = data.get('words', 0)
            print(f"  {section}: {status} ({words} words)")
    else:
        print("  No section status data")
    
    print("\n" + "=" * 50)
    print("Validation complete")

if __name__ == "__main__":
    main()
