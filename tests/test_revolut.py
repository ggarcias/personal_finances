# tests/test_revolut.py

import pytest
import pandas as pd
from io import StringIO
from src.revolut import Revolut

# Mock data simulating the content of a CSV file based on your example
mock_csv_data = """Type         ,Product ,Started Date        ,Completed Date      ,Description          ,Amount ,Fee  ,Currency ,State     ,Balance
TRANSFER     ,Savings ,2023-07-03 20:26:12 ,2023-07-03 20:26:12 ,To EUR Malos tiempos ,1.00   ,0.00 ,EUR      ,COMPLETED ,   1.00
CARD_PAYMENT ,Current ,2023-12-27 12:57:39 ,2023-12-28 13:57:42 ,Pasteleria La 28     ,-18.21 ,0.00 ,EUR      ,COMPLETED , 105.60
"""

@pytest.fixture
def revolut_instance(tmpdir):
    # Create a temporary CSV file with mock data
    csv_file = tmpdir.join("revolut_mock.csv")
    csv_file.write(mock_csv_data)
    
    # Instantiate the Revolut class with the temporary CSV path
    bank = Revolut("Revolut", str(csv_file))
    return bank

def test_parse_csv(revolut_instance):
    bank = revolut_instance
    bank.parse_csv()

    # Check if the dataframe is not empty
    assert not bank.df.empty, "The dataframe should not be empty after parsing the CSV."

    # Check if the expected columns are present
    expected_columns = ['Date', 'Amount', 'Balance', 'Bank']
    assert list(bank.df.columns) == expected_columns, f"Expected columns {expected_columns}, but got {list(bank.df.columns)}."

    # Check the data types of the columns
    assert pd.api.types.is_datetime64_any_dtype(bank.df['Date']), "The 'Date' column should be of datetime type."
    assert pd.api.types.is_numeric_dtype(bank.df['Amount']), "The 'Amount' column should be numeric."
    assert pd.api.types.is_numeric_dtype(bank.df['Balance']), "The 'Balance' column should be numeric."

    # Check if the 'Bank' column contains the correct bank name
    assert all(bank.df['Bank'] == "Revolut"), "All entries in the 'Bank' column should be 'Revolut'."

    # Additional checks for correctness of data
    assert bank.df['Amount'].iloc[0] == 1.00, "The first 'Amount' should be 1.00."
    assert bank.df['Balance'].iloc[1] == 105.60, "The second 'Balance' should be 105.60."
    assert bank.df['Date'].iloc[1] == pd.to_datetime("2023-12-28 13:57:42", format="%Y-%m-%d %H:%M:%S"), "The second 'Date' should be 2023-12-28 13:57:42."

