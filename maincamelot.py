import camelot
import pandas as pd

# Load the PDF file
file_path = '12-0K93U4.pdf'

table_regions = ['38.2, 29.8, 752, 478']
# Extract tables from page 3 to the end of the document
tables = camelot.read_pdf(file_path, pages='5-5', flavor='stream', table_areas=table_regions)

# This part of the script will help you visualize the tables that Camelot has identified
# and make sure the extraction is accurate.
# for i, table in enumerate(tables):
#     print(f"Table {i+1}:\n", table.df)
#     table.to_csv(f'table_{i+1}.csv')

# Now we have 8 headers to match our 8 columns.
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

# Process and display each table's data
for i, table in enumerate(tables):
    # # Visualize the table
    # # You can change the 'kind' to 'text', 'grid', 'line', or 'joint'
    # camelot.plot(table, kind='grid').show()
    # Set the first row as the header
    df = table.df
    
    # Check the number of columns
    if len(df.columns) == 7:
        print(f"Table {i+1} has 7 columns. Inserting a new column.")
        # Insert a blank column at position 1 (between column 0 and 1)
        df.insert(1, 'new_column_to_add', '')
        
        # Now the DataFrame has 8 columns.
        # We can apply the predefined headers.
        df.columns = headers
        
    elif len(df.columns) == 8:
        print(f"Table {i+1} has 8 columns. Headers will be applied directly.")
        # The DataFrame already has 8 columns, so just apply the predefined headers.
        df.columns = headers
    
    else:
        print(f"Table {i+1} has an unexpected number of columns: {len(df.columns)}. Skipping header assignment.")
        continue # Skip to the next table in the loop
    
    # After the conditional block, the DataFrame is ready.
    # Set the first row as the header and drop it
    df = df.iloc[1:].reset_index(drop=True)
    df = df[1:]
    
    # You can now work with this DataFrame. For example, to print it:
    # You can now work with this DataFrame. For example, to print it:
    print(f"--- Table {i+1} ---")
    print(df)
    print(len(df.columns))
    print("\n" * 2)

input()