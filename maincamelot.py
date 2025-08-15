import camelot
import pandas as pd

# Load the PDF file
file_path = '12-0K93U4.pdf'

table_regions = ['38.2, 29.8, 752, 478']
# Extract tables from page 3 to page 19
print("Reading tables from pages 3-19...")
tables = camelot.read_pdf(file_path, pages='3-19', flavor='stream', table_areas=table_regions)

# This list will hold all the processed DataFrames before we combine them.
all_processed_dfs = []

# Define the headers that will be applied to each table.
headers = [
    'Item No.',
    'Final Pay Item', # The new column
    'Item Code',
    'Item Description',
    'Unit of Measure',
    'Estimated Quantity',
    'Bid',
    'Amount'
]

# Process each table found by Camelot.
for i, table in enumerate(tables):
    df = table.df
    
    # Check the number of columns and normalize to 8 columns.
    if len(df.columns) == 7:
        # Insert a blank column at position 1.
        df.insert(1, 'new_column_to_add', '')
        df.columns = headers
        
    elif len(df.columns) == 8:
        # Apply the predefined headers directly.
        df.columns = headers
    
    else:
        print(f"Table {i+1} on page {table.page} has an unexpected number of columns: {len(df.columns)}. Skipping.")
        continue # Skip to the next table in the loop
    
    # Remove the original header row that was read as data.
    # Note: Your original code had two lines for this, which might remove an extra row of data.
    # I've kept it exactly as you wrote it.
    df = df.iloc[1:].reset_index(drop=True)
    df = df[1:]
    
    # Add the cleaned DataFrame to our list.
    all_processed_dfs.append(df)

# --- Combine all processed tables into one big table ---
if all_processed_dfs:
    # Concatenate all the DataFrames in the list into a single DataFrame.
    combined_df = pd.concat(all_processed_dfs, ignore_index=True)
    
    # --- START: ADD THIS CODE BLOCK TO MERGE BROKEN LINES ---

    # A list to keep track of the broken rows we need to remove later.
    rows_to_drop = []

    print("Checking for and merging broken description lines...")

    # Loop through the DataFrame, starting from the second row.
    for i in range(1, len(combined_df)):
        current_row = combined_df.iloc[i]
        prev_row_index = i - 1

        # --- How we identify a broken "spill-over" row ---
        # A row is considered a spill-over if it has text in 'Item Description'
        # but is missing essential data in other key columns, like 'Unit of Measure'
        # and 'Estimated Quantity'. We check this to be sure we're not merging a real item.
        
        # We convert to string and strip whitespace to handle various empty formats (NaN, '', ' ').
        desc_text = str(current_row['Item Description']).strip()
        unit_text = str(current_row['Unit of Measure']).strip()
        qty_text = str(current_row['Estimated Quantity']).strip()

        is_spill_over = (desc_text != '') and (unit_text == '') and (qty_text == '')

        # If we found a spill-over row, merge it with the row above it.
        if is_spill_over:
            # Get the description text from the previous row.
            previous_text = str(combined_df.loc[prev_row_index, 'Item Description']).strip()
            
            # Combine the text from the previous row and the current broken row.
            combined_text = previous_text + ' ' + desc_text
            
            # Update the previous row's 'Item Description' with the full, combined text.
            combined_df.loc[prev_row_index, 'Item Description'] = combined_text
            
            # Mark the current (broken) row to be dropped.
            rows_to_drop.append(i)

    # After the loop is finished, remove all the broken rows we identified.
    if rows_to_drop:
        print(f"Found and merged {len(rows_to_drop)} broken lines. 👍")
        combined_df = combined_df.drop(rows_to_drop).reset_index(drop=True)
    else:
        print("No broken lines were found.")
    
    print("\n" * 2)
    print("--- All Tables Combined ---")
    # Using to_string() to ensure all columns and rows are displayed.
    print("Exporting to CSV")
    combined_df.to_csv('12-0K93U4.csv')
    print("\n" * 2)
else:
    print("No tables were processed to be combined.")


# This will pause the script until you press Enter, so you can view the output.
input("Press Enter to exit...")
