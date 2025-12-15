import fitz
import os

def analyze_pdf(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    doc = fitz.open(path)
    print(f"Analyzing: {path}")
    print(f"Total Pages: {len(doc)}")
    
    # Track frequencies
    # xref -> {'name': name, 'type': type, 'pages': [page_nums], 'rects': [rects]}
    xref_map = {}

    for page_num, page in enumerate(doc):
        # 1. Analyze via get_xobjects (includes Forms and Images)
        xobjects = page.get_xobjects()
        for item in xobjects:
            xref = item[0]
            name = item[1]
            xo_type = item[2] # 'img' or 'form'
            
            if xref not in xref_map:
                xref_map[xref] = {
                    'name': name, 
                    'type': xo_type, 
                    'pages': [],
                }
            
            xref_map[xref]['pages'].append(page_num + 1)

        # 2. Check locations using get_images (works for images)
        # This helps us identify user images by position
        images = page.get_images(full=True)
        for img in images:
            xref = img[0]
            if xref in xref_map:
                rects = page.get_image_rects(xref)
                if 'rects' not in xref_map[xref]:
                    xref_map[xref]['rects'] = []
                # Store tuple of (Page, Rect)
                for r in rects:
                    xref_map[xref]['rects'].append((page_num + 1, r))

    print("\n" + "="*60)
    print("XOBJECT ANALYSIS REPORT")
    print("="*60)
    
    # Sort by frequency (occurrence count)
    sorted_xrefs = sorted(xref_map.items(), key=lambda x: len(x[1]['pages']), reverse=True)
    
    for xref, data in sorted_xrefs:
        count = len(data['pages'])
        is_repeated = count > 1
        
        print(f"\n[XRef: {xref}] Name: {data['name']} | Type: {data['type']}")
        print(f"  Frequency: {count} pages (Repeated: {is_repeated})")
        if count < 10:
            print(f"  Pages: {data['pages']}")
        else:
            print(f"  Pages: {data['pages'][:5]} ... (total {count})")
            
        if 'rects' in data:
            print(f"  Locations ({len(data['rects'])} instances):")
            for p_idx, r in data['rects'][:3]:
                print(f"    Page {p_idx}: x={r.x0:.1f}, y={r.y0:.1f}, w={r.width:.1f}, h={r.height:.1f}")
            if len(data['rects']) > 3:
                print("    ...")
        else:
            print("  Locations: Unknown (likely Form XObject, not direct Image)")

if __name__ == "__main__":
    # Use the filename found in the previous step
    target_file = r"d:\Work projects\Other\WaterMarkRemover\302 schedule Modified.pdf"
    
    # Redirect stdout to file to avoid encoding issues with shell redirection
    import sys
    with open("analysis_report.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        analyze_pdf(target_file)
        sys.stdout = sys.__stdout__
    
    print("Analysis complete. Saved to analysis_report.txt")
