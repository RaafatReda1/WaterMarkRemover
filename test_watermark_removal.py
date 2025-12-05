import sys
import os
sys.path.append(os.getcwd())
from src.core.cleaner import PDFCleaner

def test_watermark_removal():
    input_file = r"d:\Work projects\Other\WaterMarkRemover\cleaned_302 schedule Modified.pdf"
    output_file = r"d:\Work projects\Other\WaterMarkRemover\no_updf_watermark.pdf"
    
    cleaner = PDFCleaner()
    
    # Test with watermark removal enabled
    options = {
        'remove_links': False,
        'remove_annotations': False,
        'remove_watermarks': True
    }
    
    print(f"Cleaning: {input_file}")
    print(f"Options: {options}")
    print("\nRemoving UPDF watermark...")
    
    result = cleaner.clean_document(input_file, output_file, options)
    
    print(f"\nResult: {result}")
    
    if result['success']:
        print(f"SUCCESS!")
        print(f"  Links removed: {result.get('links_removed', 0)}")
        print(f"  Annotations removed: {result.get('annotations_removed', 0)}")
        print(f"  Watermarks removed: {result.get('watermarks_removed', 0)}")
        print(f"\nOutput saved to: {output_file}")
        print("\nPlease open the file to verify the UPDF watermark is gone!")
    else:
        print(f"ERROR: {result.get('error')}")
        if 'traceback' in result:
            print(f"\nTraceback:\n{result['traceback']}")

if __name__ == "__main__":
    test_watermark_removal()
