import os
import fitz  # PyMuPDF

class FileManager:
    def resolve_paths(self, paths):
        """
        Takes a list of paths (files or directories) and returns a list of PDF file paths.
        """
        pdf_files = []
        for path in paths:
            if os.path.isfile(path):
                if path.lower().endswith('.pdf'):
                    pdf_files.append(os.path.abspath(path))
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith('.pdf'):
                            pdf_files.append(os.path.join(root, file))
        return sorted(list(set(pdf_files)))

    def get_file_info(self, file_path):
        """
        Extracts metadata from a PDF file.
        """
        try:
            doc = fitz.open(file_path)
            info = {
                'name': os.path.basename(file_path),
                'path': file_path,
                'pages': len(doc),
                'size': os.path.getsize(file_path),
                'valid': True
            }
            doc.close()
            return info
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
