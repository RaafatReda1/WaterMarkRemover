import fitz
import sys

def comprehensive_analysis(path):
    print(f"=== COMPREHENSIVE PDF ANALYSIS ===")
    print(f"File: {path}\n")
    
    try:
        doc = fitz.open(path)
        
        for page_num, page in enumerate(doc):
            print(f"\n{'='*60}")
            print(f"PAGE {page_num + 1}")
            print(f"{'='*60}")
            
            # 1. Links
            links = list(page.get_links())
            print(f"\n[LINKS] Found: {len(links)}")
            for i, link in enumerate(links):
                print(f"  Link {i+1}: {link}")
            
            # 2. Annotations
            annots = list(page.annots()) if page.annots() else []
            print(f"\n[ANNOTATIONS] Found: {len(annots)}")
            for i, annot in enumerate(annots):
                print(f"  Annot {i+1}:")
                print(f"    Type: {annot.type}")
                print(f"    Info: {annot.info}")
                print(f"    Rect: {annot.rect}")
                # Try to get URI if it exists
                try:
                    uri = annot.get_uri()
                    if uri:
                        print(f"    URI: {uri}")
                except:
                    pass
            
            # 3. Images
            images = page.get_images(full=True)
            print(f"\n[IMAGES] Found: {len(images)}")
            for i, img in enumerate(images[:3]):  # Show first 3
                print(f"  Image {i+1}: xref={img[0]}, size={img[2]}x{img[3]}")
            
            # 4. Text content (check for URL patterns)
            text = page.get_text()
            url_keywords = ['http://', 'https://', 'www.', '.com', '.org', '.net']
            found_urls = []
            for line in text.split('\n'):
                if any(keyword in line.lower() for keyword in url_keywords):
                    found_urls.append(line.strip())
            
            if found_urls:
                print(f"\n[TEXT URLS] Found {len(found_urls)} lines with URL patterns:")
                for url in found_urls[:5]:  # Show first 5
                    print(f"  - {url}")
            
            # 5. Drawing commands (check for text in content stream)
            print(f"\n[CONTENT STREAM] Checking for watermark patterns...")
            try:
                # Get the raw content stream
                content = page.get_text("dict")
                blocks = content.get("blocks", [])
                
                # Look for text blocks that might be watermarks
                suspicious_blocks = []
                for block in blocks:
                    if block.get("type") == 0:  # Text block
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                text_content = span.get("text", "")
                                # Check if it looks like a watermark (URL, copyright, etc)
                                if any(kw in text_content.lower() for kw in ['http', 'www', '©', 'copyright', 'watermark']):
                                    suspicious_blocks.append({
                                        'text': text_content,
                                        'font': span.get('font'),
                                        'size': span.get('size'),
                                        'color': span.get('color')
                                    })
                
                if suspicious_blocks:
                    print(f"  Found {len(suspicious_blocks)} suspicious text elements:")
                    for sb in suspicious_blocks[:5]:
                        print(f"    Text: '{sb['text']}'")
                        print(f"    Font: {sb['font']}, Size: {sb['size']}, Color: {sb['color']}")
            except Exception as e:
                print(f"  Error analyzing content stream: {e}")
            
            # Only analyze first page in detail
            if page_num == 0:
                print(f"\n(Detailed analysis shown for page 1 only)")
                break
        
        doc.close()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Analyze the cleaned file to see what's still there
    analyze_path = r"d:\Work projects\Other\WaterMarkRemover\cleaned_302 schedule Modified.pdf"
    comprehensive_analysis(analyze_path)
