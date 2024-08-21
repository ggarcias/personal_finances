# tests/test_openbank.py

import pytest
import pandas as pd
from io import StringIO
from src.openbank import Openbank

# Mock data simulating the content of a CSV file based on your example
mock_csv_data = """;;;;;;;;;
;Cuentas - Movimientos;;;;;;;;
;;;;;;;;;Fecha de descarga: 28/12/2023 23:53h
;Número de Cuenta: ;;00;;;;;;
;;;;;;;;;
;Descripción:;;CUENTA NÓMINA OPEN ;;;;;;
;Titular:;;Yo yo yo;;;;;;
;Saldo:;;1.766,92 EUR;;;;;;
;Lista de Movimientos;;;;;;;;
;;;;;;;;;
;Fecha Operación;;Fecha Valor;;Concepto;;Importe;;Saldo
;27/12/2023;;27/12/2023;;BIZUM DE PEPE CONCEPTO patata ;;6,50;;1.766,92
;27/12/2023;;27/12/2023;;Supermercado Mercadona ;;13,00;;1.760,42
;;;;;;;;;
"""

@pytest.fixture
def openbank_instance(tmpdir):
    # Create a temporary CSV file with mock data
    csv_file = tmpdir.join("openbank_mock.csv")
    csv_file.write(mock_csv_data)
    
    # Instantiate the Openbank class with the temporary CSV path
    bank = Openbank("Openbank", str(csv_file))
    return bank

def test_parse_csv(openbank_instance):
    bank = openbank_instance
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
    assert all(bank.df['Bank'] == "Openbank"), "All entries in the 'Bank' column should be 'Openbank'."

    # Additional checks for correctness of data
    assert bank.df['Amount'].iloc[0] == 6.50, "The first 'Amount' should be 6.50."
    assert bank.df['Balance'].iloc[1] == 1760.42, "The second 'Balance' should be 1760.42."
    assert bank.df['Date'].iloc[0] == pd.to_datetime("27/12/2023", format="%d/%m/%Y"), "The first 'Date' should be 27/12/2023."

