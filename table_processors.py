# table_processors.py
import camelot
import pandas as pd

class BaseTableProcessor:
    TABLE_AREA = []
    HEADERS = []

    # Update the initializer to accept a page_range
    def __init__(self, file_path, page_range, plot=False):
        self.file_path = file_path
        self.page_range = page_range # Store the dynamic page range
        self.df = None
        self.plot = plot  # Default to not plotting

    def _extract_raw_dfs(self):
        if not self.page_range:
            print("Error: Page range is not set. Cannot extract.")
            return []
        
        # Use the instance variable self.page_range now
        print(f"[{self.__class__.__name__}] Reading tables from pages {self.page_range}...")
        tables = camelot.read_pdf(
            self.file_path,
            pages=self.page_range,
            table_areas=self.TABLE_AREA,
            flavor='stream',  # Use 'stream' for continuous text tables
            # ... rest of the function is the same
        )

        if(self.plot):
            for i, table in enumerate(tables):
                camelot.plot(table, kind='grid').show()

        return [table.df for table in tables]

    def _process(self, raw_dfs):
        """
        Processes the raw dataframes. This method IS MEANT TO BE OVERRIDDEN
        by each specific table class to handle its unique cleaning logic.
        """
        # A simple default implementation
        print(f"[{self.__class__.__name__}] Applying basic processing...")
        combined_df = pd.concat(raw_dfs, ignore_index=True)
        combined_df.columns = self.HEADERS
        return combined_df

    def save_to_csv(self, output_path):
        """Saves the processed DataFrame to a CSV file."""
        if self.df is not None:
            print(f"[{self.__class__.__name__}] Saving data to {output_path}...")
            self.df.to_csv(output_path, index=False)
            print("Save complete. 👍")
        else:
            print("No data to save. Run the process first.")
    
    def run(self):
        """The main execution method that orchestrates the entire process."""
        print(f"--- Starting processing for {self.__class__.__name__} ---")
        raw_dataframes = self._extract_raw_dfs()
        if not raw_dataframes:
            print("No raw tables were found. Stopping.")
            return
        self.df = self._process(raw_dataframes)
        print("--- Processing complete ---")


class LowBidderTableProcessor(BaseTableProcessor):
    """Processes the detailed 'Bid Item' tables."""
    
    # --- Configuration specific to this table type ---
    TABLE_AREA = ['38.2, 29.8, 752, 478']
    HEADERS = [
        'Item No.', 'Final Pay Item', 'Item Code', 'Item Description',
        'Unit of Measure', 'Estimated Quantity', 'Bid', 'Amount'
    ]

    def _process(self, raw_dfs):
        """Custom processing logic for Bid Item tables."""
        print(f"[{self.__class__.__name__}] Applying custom Bid Item processing...")
        
        # 1. Normalize columns (your original logic)
        processed_dfs = []
        for df in raw_dfs:
            if len(df.columns) == 7:
                df.insert(1, 'Final Pay Item', '')
            df.columns = self.HEADERS
            processed_dfs.append(df)
        
        if not processed_dfs:
            return pd.DataFrame()

        combined_df = pd.concat(processed_dfs, ignore_index=True)
        
        # 2. Merge broken description lines (your original logic)
        rows_to_drop = []
        for i in range(1, len(combined_df)):
            current_row = combined_df.iloc[i]
            prev_row_index = i - 1

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
        
        final_df = combined_df.drop(rows_to_drop).reset_index(drop=True)
        print(f"Merged {len(rows_to_drop)} broken lines.")
        return final_df

class RemainingBidderTableProcessor(BaseTableProcessor):
    """Processes the detailed 'Bid Item' tables."""
    
    # --- Configuration specific to this table type ---
    TABLE_AREA = ['37, 40, 755, 489']
    HEADERS = [
        'Item No.', 'Bid', 'Amount','Bid', 'Amount'
    ]

    def _process(self, raw_dfs):
        """Custom processing logic for Bid Item tables."""
        print(f"[{self.__class__.__name__}] Applying custom Bid Item processing...")
        
        # 1. Normalize columns (your original logic)
        processed_dfs = []
        for df in raw_dfs:
            df.columns = self.HEADERS
            processed_dfs.append(df)
        
        if not processed_dfs:
            return pd.DataFrame()

        combined_df = pd.concat(processed_dfs, ignore_index=True)

        return combined_df