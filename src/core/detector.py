import fitz
from collections import Counter

class WatermarkDetector:
    def scan_pdf(self, pdf_path):
        """
        Scans a PDF for potential watermarks.
        Returns a dict with detection results.
        """
        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            
            # results container
            detections = {
                'links': 0,
                'text_patterns': [],
                'images': 0,
                'encrypted': doc.is_encrypted
            }
            
            # 1. Link Detection & Image Counting
            link_count = 0
            all_images = []
            
            for page in doc:
                # Links
                link_count += len(list(page.get_links()))
                
                # Images (just counting for now, advanced detection would match XREFs)
                # get_images returns list of (xref, smask, width, height, bpc, colorspace, alt. colorspace, name, filter, referencer)
                imgs = page.get_images(full=False)
                all_images.extend([img[0] for img in imgs]) # Store xrefs

            detections['links'] = link_count
            
            # Image Analysis: Find images that appear on multiple pages
            # If an image xref appears on > 50% of pages, it's likely a watermark/background
            img_counts = Counter(all_images)
            repeated_images = [xref for xref, count in img_counts.items() if count > max(1, page_count * 0.5)]
            detections['images'] = len(repeated_images)

            # 2. Text Pattern Detection
            # Heuristic: Text lines that appear on > 50% of pages
            # To save time on large docs, maybe only scan first 10, middle 10, last 10? 
            # For now, let's scan all but be careful with memory.
            
            line_counter = Counter()
            
            # Optimization: Limit to first 50 pages for text pattern detection if doc is huge
            pages_to_scan = range(min(page_count, 50))
            
            for i in pages_to_scan:
                page = doc[i]
                # "blocks" -> (x0, y0, x1, y1, "text", block_no, block_type)
                text_blocks = page.get_text("blocks")
                for block in text_blocks:
                    text = block[4].strip()
                    if text and len(text) > 3: # Ignore very short artifacts
                        line_counter[text] += 1
            
            # Filter patterns
            threshold = max(1, len(pages_to_scan) * 0.5)
            detections['text_patterns'] = [
                {'text': text, 'count': count} 
                for text, count in line_counter.items() 
                if count > threshold
            ]
            
            doc.close()
            return detections
            
        except Exception as e:
            return {'error': str(e)}
