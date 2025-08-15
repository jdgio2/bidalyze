# main.py
from table_processors import LowBidderTableProcessor #, SummaryTableProcessor

PDF_FILE_PATH = '12-0K93U4.pdf'

def main():
    """Main script to run the desired table processing."""
    
    # Process the Bid Item tables
    bid_item_processor = LowBidderTableProcessor(file_path=PDF_FILE_PATH)
    bid_item_processor.run()
    bid_item_processor.save_to_csv('bid_items_output.csv')

    # When you're ready, you can process other table types
    # summary_processor = SummaryTableProcessor(file_path=PDF_FILE_PATH)
    # summary_processor.run()
    # summary_processor.save_to_csv('summary_output.csv')
    
    # ... and so on for your other two types

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")