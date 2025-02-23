import pandas as pd
import os

def clean_sales_data(file_name):
    """
    Load and clean uploaded sales data.

    Parameters:
        file_name (str): Name of the CSV file in the 'data/data/' folder.

    Returns:
        pd.DataFrame: Cleaned DataFrame or None if file not found.
    """
    # Define the correct path
    file_path = os.path.join("data", "data", file_name)

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found. Please check the path.")
        return None

    try:
        # Load CSV file
        df = pd.read_csv(file_path)

        # Check if 'Date' column exists
        if 'Date' not in df.columns:
            print("Error: 'Date' column not found in the dataset.")
            return None

        # Convert 'Date' column to datetime and drop invalid dates
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        initial_rows = len(df)
        df.dropna(subset=['Date'], inplace=True)
        dropped_rows = initial_rows - len(df)
        if dropped_rows > 0:
            print(f"⚠️ Dropped {dropped_rows} rows with invalid dates.")

        # Sort by Date
        df.sort_values(by='Date', inplace=True)

        # Fill missing numerical values with zeros
        numeric_cols = df.select_dtypes(include='number').columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        print("Data loaded and cleaned successfully!")
        return df

    except Exception as e:
        print(f"❌ An error occurred while processing the file: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Choose from existing files
    file_name = "sales_data_dummy.csv"  
    cleaned_df = clean_sales_data(file_name)
    
    if cleaned_df is not None:
        print("\nPreview of Cleaned Data:")
        print(cleaned_df.head())
