import fitz
import os
import math
from collections import defaultdict

class PDFCleaner:
    def _analyze_xobject_positions(self, doc):
        """
        Analyzes XObject positions across all pages to identify watermarks.
        
        Returns a dict with XRef as key and classification info:
        {
            xref: {
                'count': number of pages it appears on,
                'page_numbers': [list of page numbers],
                'page_coverage': percentage of pages it appears on,
                'is_watermark': boolean classification,
                'names': set of names for this XRef
            }
        }
        """
        page_count = len(doc)
        xref_data = defaultdict(lambda: {'count': 0, 'page_numbers': [], 'names': set()})
        
        # Collect all XObject data across pages
        for page_num, page in enumerate(doc, 1):  # 1-indexed page numbers
            page_xobjects = page.get_xobjects()
            for item in page_xobjects:
                xo_xref = item[0]
                xo_name = item[1]
                
                xref_data[xo_xref]['count'] += 1
                xref_data[xo_xref]['page_numbers'].append(page_num)
                xref_data[xo_xref]['names'].add(xo_name)
        
        # Analyze and classify each XObject
        results = {}
        for xref, data in xref_data.items():
            count = data['count']
            page_coverage = count / page_count if page_count > 0 else 0
            
            # Classification logic - ADJUSTED:
            # 1. Must appear on multiple pages (at least 3 for small docs, or 70% coverage)
            # 2. Lowered threshold from 80% to 70% to catch more watermarks
            min_pages = max(3, int(page_count * 0.7))
            is_watermark = count >= min_pages
            
            results[xref] = {
                'count': count,
                'page_numbers': data['page_numbers'],
                'page_coverage': page_coverage,
                'is_watermark': is_watermark,
                'names': list(data['names'])
            }
        
        return results
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
            
            # Track detailed removal information
            removed_objects = []  # List of dicts with name, pages, type info
            
            # Pre-analyze XObjects to identify watermarks using enhanced detection
            watermark_analysis = {}
            if remove_watermarks:
                watermark_analysis = self._analyze_xobject_positions(doc)
                
                # Log detected watermarks for debugging
                watermark_count = sum(1 for data in watermark_analysis.values() if data['is_watermark'])
                if watermark_count > 0:
                    print(f"[Watermark Detection] Found {watermark_count} potential watermark XObjects")
                    for xref, data in watermark_analysis.items():
                        if data['is_watermark']:
                            coverage_pct = data['page_coverage'] * 100
                            names_str = ', '.join(data['names'])
                            pages_preview = str(data['page_numbers'][:5])[1:-1]  # Show first 5 pages
                            if len(data['page_numbers']) > 5:
                                pages_preview += ', ...'
                            print(f"  - XRef {xref} ('{names_str}'): {data['count']} pages ({coverage_pct:.1f}%) - Pages: {pages_preview}")
            
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
                            
                            # 2. Remove repeated XObjects (identified as watermarks)
                            page_xobjects = page.get_xobjects()
                            
                            # Track XRef->Name mapping for watermarks on THIS page
                            # Key: (xref, name) to ensure we only remove specific instances
                            watermark_instances_on_page = set()
                            
                            for item in page_xobjects:
                                xo_xref = item[0]
                                xo_name = item[1]
                                
                                # Check if this XObject is classified as a watermark
                                if xo_xref in watermark_analysis and watermark_analysis[xo_xref]['is_watermark']:
                                    watermark_instances_on_page.add((xo_xref, xo_name))
                                    print(f"[Page {page.number}] Marking for removal: XRef {xo_xref} ('{xo_name}') - WATERMARK")
                                elif xo_xref in watermark_analysis:
                                    # This XObject was analyzed but NOT classified as watermark
                                    # Log it for debugging (this is likely a user-added image)
                                    data = watermark_analysis[xo_xref]
                                    coverage_pct = data['page_coverage'] * 100
                                    pages_str = str(data['page_numbers'][:3])[1:-1]
                                    if len(data['page_numbers']) > 3:
                                        pages_str += ', ...'
                                    print(f"[Page {page.number}] Preserving: XRef {xo_xref} ('{xo_name}'): {data['count']} pages ({coverage_pct:.1f}%) - USER IMAGE")
                            
                            # Now we need to remove ONLY the specific XRef instances
                            # Problem: We can't easily distinguish by XRef in content stream
                            # The content stream has "/Name Do" not "/XRef Do"
                            # 
                            # Solution: Check if there are MULTIPLE different XRefs with the same name
                            # If yes, we CANNOT safely remove by name alone - skip it
                            # If no, safe to remove by name
                            
                            names_with_xrefs = {}  # name -> set of xrefs on this page
                            for item in page_xobjects:
                                xo_xref = item[0]
                                xo_name = item[1]
                                if xo_name not in names_with_xrefs:
                                    names_with_xrefs[xo_name] = set()
                                names_with_xrefs[xo_name].add(xo_xref)
                            
                            # Remove watermarks where we can safely identify them
                            for xo_xref, xo_name in watermark_instances_on_page:
                                # Check if this name is ambiguous (multiple XRefs)
                                if len(names_with_xrefs[xo_name]) > 1:
                                    # UNSAFE: Same name used by multiple XRefs on this page
                                    # One might be watermark, another might be user image
                                    print(f"[WARNING] Page {page.number}: Cannot safely remove '{xo_name}' - name shared by multiple objects (XRefs: {names_with_xrefs[xo_name]})")
                                    continue
                                
                                # SAFE: This name has only one XRef on this page, and it's a watermark
                                try:
                                    name_bytes = xo_name.encode('ascii')
                                    pattern = rb'/' + re.escape(name_bytes) + rb'\s+Do'
                                    modified = re.sub(pattern, b'', modified)
                                    print(f"[Removed] Page {page.number}: Removed '{xo_name}' (XRef {xo_xref})")
                                except:
                                    pass  # Skip if name encoding fails
                            
                            # Update the content stream if modified
                            if modified != content_stream:
                                doc.update_stream(xref, modified)
                                watermarks_removed += 1
                    
                    # 3. (Optional) Corner logo detection
                    # Currently disabled to ensure safety of user-added images.
                    # We rely solely on XObject frequency detection (Method 2) above.
                    # images = page.get_images(full=True)
                    # ... (logic removed to avoid false positives and 'ghost' removal counts)
            
            # After processing all pages, collect unique removed objects summary
            # Build a set of unique XRefs that were marked as watermarks
            removed_xrefs = set()
            for xref, data in watermark_analysis.items():
                if data['is_watermark']:
                    removed_xrefs.add(xref)
            
            # Create removed_objects list with unique entries
            for xref in removed_xrefs:
                data = watermark_analysis[xref]
                # Get one of the names (they should all be the same for a given XRef)
                obj_name = data['names'][0] if data['names'] else f"XRef{xref}"
                removed_objects.append({
                    'name': obj_name,
                    'pages': data['page_numbers'],
                    'type': 'XObject watermark'
                })
            
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
                    'removed_objects': removed_objects,
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
                    'removed_objects': removed_objects,
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
