import pytest
import pandas as pd
from src.base_bank import BaseBank

class MockBank(BaseBank):
    def parse_csv(self):
        data = {'Date': ['01/06/2024 12:00:00', '02/06/2024 12:00:00'],
                'Amount': [100, -50],
                'Balance': [1000, 950]}
        self.df = pd.DataFrame(data)

def test_to_standard():
    bank = MockBank("MockBank", "mock.csv")
    bank.to_standard()
    assert not bank.df.empty
    assert 'YearMonth' in bank.df.columns

def test_calculate_metrics():
    bank = MockBank("MockBank", "mock.csv")
    bank.to_standard()
    metrics = bank.calculate_metrics()
    assert 'Total_Income' in metrics.columns
    assert 'Total_Expense' in metrics.columns
