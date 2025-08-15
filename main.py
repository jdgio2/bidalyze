# main.py
from page_finder import PageFinder
from table_processors import LowBidderTableProcessor

PDF_FILE_PATH = '11-430234.pdf'
FILE_NAME = PDF_FILE_PATH.split('.')[0]

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
        bid_item_processor.run()  # Set plot=True to visualize the tables
        bid_item_processor.save_to_csv(f'{FILE_NAME}.csv')

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")