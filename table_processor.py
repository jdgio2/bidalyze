# table_processor.py
import camelot
import pandas as pd

def extract_tables_from_pdf(file_path, page_range, table_area):
    """Extracts tables from a specific page range and area in a PDF."""
    print(f"Reading tables from pages {page_range}...")
    tables = camelot.read_pdf(
        file_path,
        pages=page_range,
        flavor='stream',
        table_areas=table_area
    )
    return [table.df for table in tables]

def normalize_and_clean_tables(raw_dfs, headers):
    """Normalizes column count and sets headers for a list of DataFrames."""
    processed_dfs = []
    for i, df in enumerate(raw_dfs):
        if len(df.columns) == len(headers) - 1: # Assumes 7 columns need one added
            df.insert(1, 'Final Pay Item', '') # Insert the specific empty column
            df.columns = headers
            processed_dfs.append(df)
        elif len(df.columns) == len(headers):
            df.columns = headers
            processed_dfs.append(df)
        else:
            print(f"Table {i+1} has an unexpected number of columns: {len(df.columns)}. Skipping.")
            continue
    return processed_dfs

def merge_broken_lines(df):
    """Merges description lines that spill over into the next row."""
    if df.empty:
        return df

    rows_to_drop = []
    print("Checking for and merging broken description lines...")

    for i in range(1, len(df)):
        current_row = df.iloc[i]
        prev_row_index = i - 1

        desc_text = str(current_row['Item Description']).strip()
        unit_text = str(current_row['Unit of Measure']).strip()
        qty_text = str(current_row['Estimated Quantity']).strip()

        is_spill_over = (desc_text != '') and (unit_text == '') and (qty_text == '')

        if is_spill_over:
            previous_text = str(df.loc[prev_row_index, 'Item Description']).strip()
            combined_text = f"{previous_text} {desc_text}"
            df.loc[prev_row_index, 'Item Description'] = combined_text
            rows_to_drop.append(i)

    if rows_to_drop:
        print(f"Found and merged {len(rows_to_drop)} broken lines. 👍")
        df = df.drop(rows_to_drop).reset_index(drop=True)
    else:
        print("No broken lines were found.")
        
    return df