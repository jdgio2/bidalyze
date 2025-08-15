# page_finder.py
import fitz  # PyMuPDF

class PageFinder:
    """
    Scans a PDF document to find the start and end pages
    for different types of content based on keywords.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = fitz.open(file_path)
        print(f"Opened '{file_path}' with {self.doc.page_count} pages.")

    def find_page_range(self, start_keyword, end_keyword):
        """
        Finds the start and end page for a section defined by keywords.
        
        Returns:
            A string like 'start-end' (e.g., '3-20') or None if not found.
        """
        start_page = None
        end_page = None

        for i, page in enumerate(self.doc):
            text = page.get_text().lower() # Search case-insensitively
            
            # Look for the start of the section
            if start_keyword.lower() in text and start_page is None:
                start_page = i + 1 # Page numbers are 1-based
            
            # If we've found the start, now look for the end
            if start_page is not None and end_keyword.lower() in text:
                end_page = i
                break # Stop once we find the end keyword
        
        # If we found a start but no end, assume it goes to the end of the doc
        if start_page and not end_page:
            end_page = self.doc.page_count

        if start_page and end_page:
            print(f"Found section '{start_keyword}' from page {start_page} to {end_page}.")
            return f"{start_page}-{end_page}"
        
        print(f"Warning: Could not find page range for '{start_keyword}'.")
        return None

    def close(self):
        """Closes the PDF document."""
        self.doc.close()