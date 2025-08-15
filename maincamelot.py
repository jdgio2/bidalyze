import camelot
import pandas as pd

# Load the PDF file
file_path = '12-0K93U4.pdf'

table_regions = ['35, 134, 760, 600']
# Extract tables from page 3 to the end of the document
tables = camelot.read_pdf(file_path, pages='3-3', flavor='stream', table_areas=table_regions)

# This part of the script will help you visualize the tables that Camelot has identified
# and make sure the extraction is accurate.
# for i, table in enumerate(tables):
#     print(f"Table {i+1}:\n", table.df)
#     table.to_csv(f'table_{i+1}.csv')

# Process and display each table's data
for i, table in enumerate(tables):
    # Set the first row as the header
    df = table.df
    df.columns = df.iloc[0]
    df = df[1:]
    
    # You can now work with this DataFrame. For example, to print it:
    # You can now work with this DataFrame. For example, to print it:
    print(f"--- Table {i+1} ---")
    print(df)
    print("\n" * 2)