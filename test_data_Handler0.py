# Author: Nathaniel and  Saif
# Date: 11/26/2024
# Description: This module contains tests for the DataHandler class.

import pytest
from dataHandler import DataHandler  # Correct module name
import os
import pandas as pd

@pytest.fixture
def sample_file_path():
    """Fixture to provide a sample CSV file path."""
    # Dynamically resolve the absolute path to avoid path issues
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "AllCarriers.csv"))

@pytest.fixture
def data_handler(sample_file_path):
    """Fixture to initialize a DataHandler instance."""
    return DataHandler(sample_file_path)

def test_load_data(data_handler):
    """Test if data loads successfully."""
    data_handler.load_data()
    assert isinstance(data_handler.data, pd.DataFrame), "Data should be a Pandas DataFrame after loading."

def test_clean_data(data_handler):
    """Test if data cleaning works as expected."""
    data_handler.load_data()
    cleaned_data = data_handler.clean_data()
    assert cleaned_data["DOMESTIC"].dtype == "int64", "DOMESTIC column should be of type int64 after cleaning."
    assert cleaned_data["INTERNATIONAL"].dtype == "int64", "INTERNATIONAL column should be of type int64 after cleaning."
    assert cleaned_data["TOTAL"].dtype == "int64", "TOTAL column should be of type int64 after cleaning."
