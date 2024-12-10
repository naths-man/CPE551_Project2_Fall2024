import pandas as pd
import os

class DataHandler:
    """
    Class to handle data operations such as loading, cleaning, and basic analysis.
    """

    def __init__(self, folder_path: str):
        """
        Initializes the DataHandler with a folder path.

        Args:
            folder_path (str): Path to the folder containing carrier CSV files.
        """
        self.folder_path = folder_path
        self.data = {}
        self.available_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    def load_data(self):
        """
        Loads data from all CSV files in the folder into a dictionary of Pandas DataFrames.

        Raises:
            FileNotFoundError: If no CSV files are found in the folder.
        """
        if not self.available_files:
            raise FileNotFoundError(f"No CSV files found in the folder: {self.folder_path}")

        for file in self.available_files:
            file_path = os.path.join(self.folder_path, file)
            try:
                self.data[file] = pd.read_csv(file_path)
                print(f"Loaded {file}")
            except Exception as e:
                print(f"Failed to read {file}. Error: {e}")

    def clean_data(self):
        """
        Cleans the data for all loaded DataFrames by converting numerical columns to integers and removing commas.

        Returns:
            dict: A dictionary of cleaned DataFrames.
        """
        cleaned_data = {}
        for file, df in self.data.items():
            try:
                columns_to_clean = ["DOMESTIC", "INTERNATIONAL", "TOTAL"]
                for column in columns_to_clean:
                    if column in df.columns:
                        # Ensure the column is of string type before replacing
                        df[column] = df[column].astype(str).str.replace(",", "")
                        # Convert to numeric and handle errors
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(int)
                cleaned_data[file] = df
            except Exception as e:
                print(f"Error cleaning data in {file}: {e}")

        self.data = cleaned_data

    def get_summary(self):
        """
        Provides a summary of all loaded data.

        Returns:
            dict: A dictionary of summaries for each DataFrame.
        """
        summaries = {}
        for file, df in self.data.items():
            try:
                summaries[file] = df.describe()
            except Exception as e:
                print(f"Error summarizing data in {file}: {e}")
        return summaries

# Example usage:
if __name__ == "__main__":
    folder_path = "." # The directory containing airline files
    handler = DataHandler(folder_path)

    try:
        handler.load_data()
        handler.clean_data()
        summaries = handler.get_summary()
        for file, summary in summaries.items():
            print(f"Summary for {file}:\n{summary}")
    except Exception as e:
        print(f"An error occurred: {e}")
