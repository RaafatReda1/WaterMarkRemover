import fitz
import sys

def deep_watermark_analysis(path):
    print(f"=== DEEP WATERMARK ANALYSIS ===")
    print(f"File: {path}\n")
    
    try:
        doc = fitz.open(path)
        page = doc[0]  # First page
        
        print("="*60)
        print("ANALYZING PAGE 1 CONTENT")
        print("="*60)
        
        # 1. Get all text with positions
        print("\n[TEXT BLOCKS WITH POSITIONS]")
        blocks = page.get_text("dict")["blocks"]
        
        for i, block in enumerate(blocks):
            if block["type"] == 0:  # Text block
                bbox = block["bbox"]
                print(f"\nBlock {i+1}: Position ({bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f})")
                
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        font = span["font"]
                        size = span["size"]
                        
                        # Check if this looks like the UPDF watermark
                        if "updf" in text.lower() or "www" in text.lower():
                            print(f"  >>> WATERMARK FOUND: '{text}'")
                            print(f"      Font: {font}, Size: {size}")
                            print(f"      Color: {span.get('color', 'N/A')}")
                            print(f"      Position: {span['bbox']}")
        
        # 2. Get images with positions
        print("\n\n[IMAGES WITH POSITIONS]")
        images = page.get_images(full=True)
        
        for i, img in enumerate(images):
            xref = img[0]
            
            # Get image position
            img_rects = page.get_image_rects(xref)
            
            print(f"\nImage {i+1}: xref={xref}")
            print(f"  Size: {img[2]}x{img[3]}")
            
            for rect in img_rects:
                print(f"  Position: {rect}")
                
                # Check if image is in top area (likely watermark)
                if rect.y0 < 200:  # Top 200 points
                    print(f"  >>> POTENTIAL WATERMARK (top of page)")
        
        # 3. Check for XObjects (Form XObjects can be watermarks)
        print("\n\n[XOBJECTS]")
        xobjects = page.get_xobjects()
        print(f"Found {len(xobjects)} XObjects")
        for xobj in xobjects:
            print(f"  XObject: {xobj}")
        
        doc.close()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Need the ORIGINAL file, not the cleaned one
    # Let's check what files we have
    import os
    pdf_files = [f for f in os.listdir(r"d:\Work projects\Other\WaterMarkRemover") if f.endswith('.pdf')]
    print("Available PDF files:")
    for f in pdf_files:
        print(f"  - {f}")
    
    print("\n" + "="*60 + "\n")
    
    # Analyze the cleaned file to see the watermark structure
    analyze_path = r"d:\Work projects\Other\WaterMarkRemover\cleaned_302 schedule Modified.pdf"
    deep_watermark_analysis(analyze_path)
