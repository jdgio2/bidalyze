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

    def find_bid_info(self):
        """
        Finds the information for the bid contained in the first page, specifically, the number of bidders and the name of the project
        """
        first_page = self.doc[0]
        text_instances = first_page.search_for("Number of Bidders:")

        if text_instances:
            # Get the first instance found on the page
            text_rect = text_instances[0]

            # Define a new rectangle to the right of the found text
            # We start at the right edge of the found text and go a small distance
            # to the right, maintaining the same vertical (y) position.
            # The value 100 is an estimated width for the "tab space".
            # You might need to adjust this value.
            number_rect = fitz.Rect(
                text_rect.x1 + 10,  # Start a little bit to the right of the found text
                text_rect.y0 - 2,    # A small vertical offset to capture the number
                text_rect.x1 + 100, # A generous width for the number
                text_rect.y1 + 2     # A small vertical offset
            )
            
            # Extract the text from this new rectangle
            number_text = first_page.get_text(clip=number_rect).strip()

             # Filter out non-digit characters and convert to an integer
            cleaned_text = "".join(filter(str.isdigit, number_text))
            if cleaned_text:
                return int(cleaned_text)
        return None

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
            if start_page is not None and start_keyword.lower() not in text:
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