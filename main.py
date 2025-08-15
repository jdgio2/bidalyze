# main.py
import pandas as pd
import config
import table_processor

def main():
    """Main workflow to extract, process, and save table data from a PDF."""
    
    # 1. Get settings from the config file
    # For now, we use one table type. Later, you can loop through multiple configs.
    settings = config.TABLE_TYPE_1_CONFIG
    
    # --- THIS IS WHERE YOUR NEW LOGIC WOULD GO ---
    # Example: You could call a function to find page boundaries first
    # page_ranges = find_page_boundaries(config.PDF_FILE_PATH)
    # Then loop through the ranges...
    
    # 2. Extract raw tables from the PDF
    raw_dataframes = table_processor.extract_tables_from_pdf(
        file_path=config.PDF_FILE_PATH,
        page_range=settings['page_range'],
        table_area=settings['table_area']
    )
    
    # 3. Clean and normalize the tables
    cleaned_dataframes = table_processor.normalize_and_clean_tables(
        raw_dfs=raw_dataframes,
        headers=settings['headers']
    )

    if not cleaned_dataframes:
        print("No tables were processed.")
        return

    # 4. Combine into a single DataFrame
    combined_df = pd.concat(cleaned_dataframes, ignore_index=True)
    
    # 5. Merge broken description lines
    final_df = table_processor.merge_broken_lines(combined_df)
    
    # 6. Save the final output
    print("\n--- Exporting to CSV ---")
    final_df.to_csv(config.OUTPUT_CSV_PATH, index=False)
    print(f"Successfully saved data to {config.OUTPUT_CSV_PATH}")


if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")