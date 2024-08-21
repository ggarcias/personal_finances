# src/revolut.py

import pandas as pd
from src.base_bank import BaseBank


class Revolut(BaseBank):
    def parse_csv(self):
        df = pd.read_csv(self.csv_path, delimiter=',', header=0, encoding='utf-8')
        df.columns = [col.strip() for col in df.columns]
        df['Date'] = pd.to_datetime(df['Completed Date'].str.strip(), format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
        df.dropna(subset=['Date', 'Amount', 'Balance'], inplace=True)
        df.sort_values('Date', inplace=True)

        df['Bank'] = 'Revolut'
        
        self.df = df[['Date', 'Amount', 'Balance', 'Description', 'Bank']]