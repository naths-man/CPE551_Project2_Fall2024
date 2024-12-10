import pytest
import pandas as pd
from guiManager import GUIManager  # Directly import GUIManager from the same directory

@pytest.fixture
def sample_data():
    """Fixture to provide sample data."""
    return pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar"],
        "DOMESTIC": [1, 2, 3],
        "INTERNATIONAL": [4, 5, 6],
        "TOTAL": [5, 7, 9]
    })

def test_gui_initialization(sample_data):
    """Test if GUIManager initializes correctly."""
    gui = GUIManager(sample_data)
    assert gui.data.equals(sample_data), "GUIManager should store the provided data correctly."
    assert gui.app is not None, "Dash app instance should not be None."