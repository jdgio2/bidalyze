# main.py
from page_finder import PageFinder
from table_processors import LowBidderTableProcessor

PDF_FILE_PATH = '12-0K93U4.pdf'

def main():
    """Main script to find page ranges and then process tables."""
    
    # 1. Use the PageFinder to discover where the tables are
    finder = PageFinder(file_path=PDF_FILE_PATH)
    
    # Define keywords that mark the beginning and end of your sections
    bid_item_range = finder.find_page_range(
        start_keyword="contract proposal of low bidder", # Example keyword
        end_keyword="summary of remaining bidders"   # Example keyword
    )
    
    # You could find other ranges here too
    # summary_range = finder.find_page_range(...)
    
    finder.close() # Good practice to close the file

    # 2. If the range was found, create a processor and run it
    if bid_item_range:
        bid_item_processor = LowBidderTableProcessor(
            file_path=PDF_FILE_PATH,
            page_range=bid_item_range # Pass the discovered range here
        )
        bid_item_processor.run()
        bid_item_processor.save_to_csv('bid_items_output.csv')

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")