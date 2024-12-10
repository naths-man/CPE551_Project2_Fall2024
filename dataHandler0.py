import pandas as pd
import os


class DataHandler:
    """
    Class to handle data operations such as loading, cleaning, and basic analysis.
    """

    def __init__(self, file_path: str):
        """
        Initializes the DataHandler with a file path.

        Args:
            file_path (str): Path to the CSV file containing carrier data.
        """
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """
        Loads data from the CSV file into a Pandas DataFrame.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file is not a valid CSV.
        """
        print(f"Attempting to load file from: {self.file_path}")
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file at {self.file_path} was not found.")

        try:
            self.data = pd.read_csv(self.file_path)
        except Exception as e:
            raise ValueError(f"Failed to read CSV file. Error: {e}")

    def clean_data(self):
        """
        Cleans the data by converting numerical columns to integers and removing commas.

        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        if self.data is None:
            raise ValueError("Data has not been loaded. Call load_data() first.")

        # Define columns to clean
        columns_to_clean = ["DOMESTIC", "INTERNATIONAL", "TOTAL"]

        for column in columns_to_clean:
            self.data[column] = self.data[column].str.replace(",", "").astype(int)

        return self.data

    def get_summary(self):
        """
        Provides a summary of the loaded data.

        Returns:
            str: Summary of the DataFrame.
        """
        if self.data is None:
            raise ValueError("Data has not been loaded. Call load_data() first.")

        return self.data.describe()
