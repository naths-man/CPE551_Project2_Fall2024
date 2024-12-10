from dataHandler import DataHandler
from guiManager import GUIManager
import os

def main():
    """
    Main function to load data, clean it, and launch the GUI.
    """
    # Dynamically resolve the absolute path to the CSV file
    project_root = os.path.dirname(os.path.abspath(__file__))  # Current script's directory
    file_path = os.path.join(project_root, "AllCarriers.csv")  # Adjust to match actual file location

    # Debugging: Print the resolved file path
    print(f"Resolved file path: {file_path}")

    # Initialize the DataHandler
    data_handler = DataHandler(file_path)

    try:
        # Load and clean the data
        data_handler.load_data()
        cleaned_data = data_handler.clean_data()

        print("Data loaded and cleaned successfully!")
    except Exception as e:
        print(f"Error loading or cleaning data: {e}")
        return

    # Initialize and run the GUIManager with cleaned data
    gui_manager = GUIManager(cleaned_data)
    gui_manager.run()

if __name__ == "__main__":
    main()