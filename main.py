# Author: Nathaniel and Saif
# Date: 11/26/2024
# Description: Main script for running the carrier data analysis program. Integrates DataHandler and GUIManager.

from dataHandler import DataHandler
from guiManager import GUIManager
import os

def main():
    """
    Main function to initialize data handling and the graphical user interface.
    """
    # Dynamically resolve the absolute path to the folder containing the CSV files
    project_root = os.path.dirname(os.path.abspath(__file__))  # Current script's directory
    data_folder_path = project_root  # Assuming all CSV files are in the same directory as the script

    # Debugging: Print the resolved folder path
    print(f"Resolved data folder path: {data_folder_path}")

    # Initialize the DataHandler with the folder path
    data_handler = DataHandler(data_folder_path)

    try:
        # Load and clean the data
        data_handler.load_data()
        data_handler.clean_data()
        cleaned_data = data_handler.data

        print("Data loaded and cleaned successfully!")
    except Exception as e:
        print(f"Error loading or cleaning data: {e}")
        return

    # Initialize and run the GUIManager with the cleaned data
    gui_manager = GUIManager(cleaned_data)
    gui_manager.run()

if __name__ == "__main__":
    main()
