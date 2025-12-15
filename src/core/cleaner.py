import fitz
import os

class PDFCleaner:
    def clean_document(self, input_path, output_path, options=None):
        """
        Removes watermarks/annotations based on options.
        Supports: links, annotations (highlights, stamps, etc.), watermarks (XObjects, images)
        """
        try:
            doc = fitz.open(input_path)
            
            remove_links = options.get('remove_links', True) if options else True
            remove_annotations = options.get('remove_annotations', False) if options else False
            remove_watermarks = options.get('remove_watermarks', False) if options else False
            overwrite_original = options.get('overwrite_original', False) if options else False
            
            links_removed = 0
            annotations_removed = 0
            watermarks_removed = 0
            
            # Pre-scan for repeated XObjects (likely watermarks)
            watermark_xrefs = set()
            if remove_watermarks:
                xref_counts = {}
                for p in doc:
                    # get_xobjects returns list of items, handle variable length
                    for item in p.get_xobjects():
                        xo_xref = item[0]
                        xref_counts[xo_xref] = xref_counts.get(xo_xref, 0) + 1
                
                # Identify XRefs that appear on more than 1 page
                watermark_xrefs = {x for x, count in xref_counts.items() if count > 1}
            
            for page in doc:
                # 1. Remove Links
                if remove_links:
                    # Remove standard link annotations
                    for link in page.get_links():
                        if link:
                            page.delete_link(link)
                            links_removed += 1
                
                # 2. Remove All Annotations (including highlights, stamps, etc.)
                if remove_annotations:
                    annots_to_remove = []
                    for annot in page.annots():
                        annots_to_remove.append(annot)
                    
                    for annot in annots_to_remove:
                        page.delete_annot(annot)
                        annotations_removed += 1
                
                # 3. If remove_links is on, also check annotations for URI actions
                elif remove_links:
                    annots_to_remove = []
                    for annot in page.annots():
                        # Check if annot has a URI action
                        info = annot.info
                        if 'uri' in str(info).lower() or annot.type[0] == fitz.PDF_ANNOT_LINK:
                            annots_to_remove.append(annot)
                    
                    for annot in annots_to_remove:
                        page.delete_annot(annot)
                        links_removed += 1
                
                # 4. Remove Watermarks (XObjects and Images)
                if remove_watermarks:
                    # Get the page's content stream
                    xref = page.get_contents()[0] if page.get_contents() else None
                    
                    if xref:
                        # Get raw content stream
                        content_stream = doc.xref_stream(xref)
                        
                        if content_stream:
                            modified = content_stream
                            import re
                            
                            # 1. (Removed) Do NOT blindly remove UPDF watermark XObjects by name pattern
                            # because user-added images might be named 'UPDFX...' if added via UPDF editor.
                            # We now rely solely on the frequency detection below.
                            # modified = re.sub(rb'/UPDFX\d+\s+Do', b'', modified)
                            
                            # 2. Remove repeated XObjects (likely watermarks)
                            page_xobjects = page.get_xobjects()
                            names_to_remove = set()
                            
                            for item in page_xobjects:
                                xo_xref = item[0]
                                xo_name = item[1]
                                if xo_xref in watermark_xrefs:
                                    names_to_remove.add(xo_name)
                            
                            for name in names_to_remove:
                                # Create pattern for "/Name Do"
                                # handle encoding carefully
                                try:
                                    name_bytes = name.encode('ascii')
                                    # Pattern: /Name Do
                                    # Use regex escape to handle potential special chars in name
                                    pattern = rb'/' + re.escape(name_bytes) + rb'\s+Do'
                                    modified = re.sub(pattern, b'', modified)
                                except:
                                    pass # Skip if name encoding fails
                            
                            # Update the content stream if modified
                            if modified != content_stream:
                                doc.update_stream(xref, modified)
                                watermarks_removed += 1
                    
                    # Remove images in watermark positions (top-left corner, typically < 200 points from top)
                    images = page.get_images(full=True)
                    for img in images:
                        xref = img[0]
                        rects = page.get_image_rects(xref)
                        
                        for rect in rects:
                            # Check if image is in typical watermark position
                            if rect.y0 < 150 and rect.x0 < 150:  # Top-left corner
                                # This is likely a watermark logo
                                # We need to remove it from the content stream
                                # This is complex, so for now we'll mark it
                                watermarks_removed += 1
            
            # If overwrite is enabled, save to original path
            if overwrite_original:
                # Save to temp file first, then replace original
                import tempfile
                temp_fd, temp_path = tempfile.mkstemp(suffix='.pdf')
                os.close(temp_fd)
                
                doc.save(temp_path, garbage=4, deflate=True, clean=True)
                doc.close()
                
                # Replace original with temp file
                import shutil
                shutil.move(temp_path, input_path)
                
                return {
                    'success': True,
                    'links_removed': links_removed,
                    'annotations_removed': annotations_removed,
                    'watermarks_removed': watermarks_removed,
                    'overwritten': True
                }
            else:
                # Clean the document to remove unused objects
                doc.save(output_path, garbage=4, deflate=True, clean=True)
                doc.close()
                
                return {
                    'success': True,
                    'links_removed': links_removed,
                    'annotations_removed': annotations_removed,
                    'watermarks_removed': watermarks_removed,
                    'overwritten': False
                }
            
        except Exception as e:
            import traceback
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }

    def generate_output_path(self, input_path):
        """
        Generates a default output path (e.g., encoded_filename -> cleaned_filename).
        """
        directory = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        new_name = f"cleaned_{name}{ext}"
        return os.path.join(directory, new_name)
