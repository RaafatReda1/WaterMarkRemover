import fitz
import sys

def analyze_pdf(path):
    print(f"Analyzing: {path}")
    try:
        doc = fitz.open(path)
        for i, page in enumerate(doc):
            print(f"--- Page {i+1} ---")
            
            # Check Links
            links = list(page.get_links())
            print(f"Links found: {len(links)}")
            
            # Check Annotations
            annots = list(page.annots()) if page.annots() else []
            print(f"Annotations found: {len(annots)}")
            for annot in annots:
                print(f"  Annot: {annot.type} (Info: {annot.info})")
            
            # Check Text for URLs
            text = page.get_text()
            if "http" in text or "www" in text:
                print("  [POTENTIAL TEXT LINK FOUND IN CONTENT]")
                # Print the line containing http
                for line in text.split('\n'):
                    if "http" in line or "www" in line:
                        print(f"    Text content: {line.strip()}")
                
        doc.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_pdf(r"d:\Work projects\Other\WaterMarkRemover\cleaned_302 schedule Modified.pdf")
