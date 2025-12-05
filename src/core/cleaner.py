import fitz
import os

class PDFCleaner:
    def clean_document(self, input_path, output_path, options=None):
        """
        Removes watermarks/annotations based on options.
        Phase 1: Support link removal.
        """
        try:
            doc = fitz.open(input_path)
            
            remove_links = options.get('remove_links', True) if options else True
            
            links_removed = 0
            
            for page in doc:
                if remove_links:
                    # 'Link' annotations usually; we can iterate all annotations/links
                    # In PyMuPDF, links are separate from generic annotations in some contexts, but let's check both
                    
                    # 1. Remove Link items
                    for link in page.get_links():
                        if link:
                            page.delete_link(link)
                            links_removed += 1
            
            doc.save(output_path)
            doc.close()
            
            return {
                'success': True,
                'links_removed': links_removed
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
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
