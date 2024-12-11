# Author: Nathaniel and Saif
# Date: 11/26/2024
# Description: This module contains tests for the DataHandler class.

import pytest
from dataHandler import DataHandler
import os
import pandas as pd


@pytest.fixture
def sample_folder_path():
    """Fixture to provide the folder containing CSV files."""
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def data_handler(sample_folder_path):
    """Fixture to initialize a DataHandler instance."""
    return DataHandler(sample_folder_path)


def test_load_all_csv_files(data_handler):
    """Test if all CSV files in the folder load successfully, including AllCarriers.csv."""
    data_handler.load_data()
    assert "AllCarriers.csv" in data_handler.data, "'AllCarriers.csv' not loaded."
    assert len(data_handler.data) > 0, "No CSV files loaded."
    assert all(isinstance(df, pd.DataFrame) for df in data_handler.data.values()), "All data should be Pandas DataFrames."


def test_data_columns_presence(data_handler):
    """Test if required columns exist in the data."""
    data_handler.load_data()
    for df in data_handler.data.values():
        assert all(column in df.columns for column in ["DOMESTIC", "INTERNATIONAL", "TOTAL"]), \
            "Missing one or more required columns in the data."


def test_value_in_data_34557(data_handler):
    """Test if any of the files contain the number '34557'."""
    data_handler.load_data()
    contains_value = False
    for df in data_handler.data.values():
        if (df.isin([34557]).any()).any():
            contains_value = True
            break
    assert contains_value, "The number '34557' was not found in any of the data files."


def test_value_in_data_500000(data_handler):
    """Test if any of the files contain the number '500000'."""
    data_handler.load_data()
    contains_value = False
    for df in data_handler.data.values():
        if (df.isin([500000]).any()).any():
            contains_value = True
            break
    assert not contains_value, "The number '500000' was not found in any of the data files."


def test_summary_statistics(data_handler):
    """Test if summary statistics return expected structure."""
    data_handler.load_data()
    data_handler.clean_data()
    summaries = data_handler.get_summary()
    assert isinstance(summaries, dict), "Summary should be a dictionary."
    for summary in summaries.values():
        assert isinstance(summary, pd.DataFrame), "Each summary should be a Pandas DataFrame."


def test_years_in_allcarriers(data_handler):
    """Test if specific years are present in AllCarriers.csv."""
    data_handler.load_data()
    df = data_handler.data.get("AllCarriers.csv")
    assert df is not None, "'AllCarriers.csv' is missing."
    assert df["YEAR"].between(2018, 2023).all(), "All years in 'AllCarriers.csv' should be between 2018 and 2023."


def test_months_in_allcarriers(data_handler):
    """Test if all months (January to December) are present in AllCarriers.csv."""
    expected_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data_handler.load_data()
    df = data_handler.data.get("AllCarriers.csv")
    assert df is not None, "'AllCarriers.csv' is missing."
    assert all(month in df["MONTH"].unique() for month in expected_months), "Some months are missing in 'AllCarriers.csv'."
