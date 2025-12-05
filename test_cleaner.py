import sys
import os
sys.path.append(os.getcwd())
from src.core.cleaner import PDFCleaner

def test_cleaner():
    input_file = r"d:\Work projects\Other\WaterMarkRemover\cleaned_302 schedule Modified.pdf"
    output_file = r"d:\Work projects\Other\WaterMarkRemover\test_no_annotations.pdf"
    
    cleaner = PDFCleaner()
    
    # Test with annotations removal enabled
    options = {
        'remove_links': True,
        'remove_annotations': True
    }
    
    print(f"Cleaning: {input_file}")
    print(f"Options: {options}")
    
    result = cleaner.clean_document(input_file, output_file, options)
    
    print(f"\nResult: {result}")
    
    if result['success']:
        print(f"✓ Success!")
        print(f"  Links removed: {result.get('links_removed', 0)}")
        print(f"  Annotations removed: {result.get('annotations_removed', 0)}")
        print(f"\nOutput saved to: {output_file}")
    else:
        print(f"✗ Error: {result.get('error')}")

if __name__ == "__main__":
    test_cleaner()
