# src/openbank.py

import pandas as pd
from src.base_bank import BaseBank


class Openbank(BaseBank): 
    def parse_csv(self):
        df = pd.read_csv(self.csv_path, sep=";", skiprows=10)
        num_cols = len(df.columns)
        df.columns = ["Col" + str(i) for i in range(num_cols)]
        df.ffill(inplace=True)
        nan_cols = [col for col in df.columns if df[col].isnull().all()]
        df.drop(columns=nan_cols, inplace=True)
        df.dropna(how='all', axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.columns = ["Fecha Operación", "Fecha Valor", "Concepto", "Importe", "Saldo"]
        df['Date'] = pd.to_datetime(df['Fecha Operación'], format="%d/%m/%Y", errors='coerce')
        df['Amount'] = pd.to_numeric(df['Importe'].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        df['Balance'] = pd.to_numeric(df['Saldo'].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        df = df.dropna(subset=['Date'])
        df['Description'] = df['Concepto']

        df['Bank'] = 'Openbank'
        self.df = df[['Date', 'Amount', 'Balance', 'Description', 'Bank']]