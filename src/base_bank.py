import os
import pandas as pd
from abc import ABC, abstractmethod
from transformers import pipeline
from src.financial_functions import filter_date_range

class BaseBank(ABC):
    def __init__(self, name, csv_path):
        self.df = None
        self.name = name
        self.csv_path = csv_path
        self.datetime_format = "%d/%m/%Y %H:%M:%S"
        
        self.classifier = pipeline('zero-shot-classification', model='typeform/distilbert-base-uncased-mnli')
        
        self.candidate_labels = [
            "Groceries",      # Supermarkets, food shopping
            "Dining",         # Restaurants, cafes, takeout
            "Transport",      # Public transport, taxis, fuel
            "Shopping",       # Clothes, electronics, general shopping
            "Entertainment",  # Movies, concerts, streaming services
            "Utilities",      # Electricity, water, gas, internet
            "Rent",           # Rent payments
            "Healthcare",     # Doctor visits, medications, insurance
            "Insurance",      # Auto, home, health insurance
            "Savings",        # Savings accounts, investments
            "Transfer",       # Transfers to other accounts
            "Subscriptions",  # Regular subscriptions (e.g., Netflix, gym)
            "Education",      # Tuition, books, courses
            "Gifts & Donations",  # Charitable donations, gifts to others
            "Travel",         # Flights, hotels, vacations
            "Personal Care",  # Salons, cosmetics, grooming
            "Other"           # Miscellaneous
        ]

    @abstractmethod
    def parse_csv(self):
        pass

    def calculate_metrics(self, start_date=None, end_date=None):
        self.df = filter_date_range(self.df, start_date, end_date)
        return self.average_metric_per_month()

    def average_metric_per_month(self):
        self.df['Income'] = self.df['Amount'].apply(lambda x: x if x > 0 else 0)
        self.df['Expense'] = self.df['Amount'].apply(lambda x: x if x < 0 else 0)
        metrics_per_month = self.df.groupby('YearMonth').agg({
            'Income': 'sum',
            'Expense': 'sum',
            'Balance': ['first', 'last']
        }).reset_index()
        metrics_per_month.columns = ['YearMonth', 'Total_Income', 'Total_Expense', 'Balance_Beginning', 'Balance_Ending']
        metrics_per_month['Total_Expense'] = metrics_per_month['Total_Expense'].abs()
        return metrics_per_month
    
    def categorize_expenses(self):
        try:
            # Process descriptions in batches for faster performance
            batch_size = 32  # Adjust the batch size depending on your memory constraints
            descriptions = self.df['Description'].tolist()
            categories = []

            for i in range(0, len(descriptions), batch_size):
                batch_descriptions = descriptions[i:i+batch_size]
                results = self.classifier(batch_descriptions, self.candidate_labels)
                categories.extend([result['labels'][0] for result in results])

            self.df['Category'] = categories

        except Exception as e:
            print(f"Error categorizing expenses for {self.name}: {e}")

    def categorize_description(self, description):
        result = self.classifier(description, self.candidate_labels)
        return result['labels'][0]  # Return the category with the highest score

    def save_data(self, df, out_name, output_folder="."):
        try:
            os.makedirs(output_folder, exist_ok=True)
            df.to_csv(f"{output_folder}/{out_name}.csv", index=False)
        except Exception as e:
            print(f"Error saving {out_name}: {e}")

    def print_highest_expense(self):
        try:
            expense_df = self.df[self.df['Amount'] < 0].copy()
            top_expenses = expense_df.sort_values(by='Amount').head(5)
            if not top_expenses.empty:
                print("Top 5 Highest Expenses:")
                for index, expense in top_expenses.iterrows():
                    print(f"Date: {expense['Date']}, Amount: {expense['Amount']}, Balance: {expense['Balance']}")
            else:
                print("No expense data available.")
        except KeyError:
            print(f"Dataframe is missing required columns.")
        except Exception as e:
            print(f"Error processing highest expenses: {e}")

    def to_standard(self):
        try:
            self.parse_csv()
            self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
            self.df.sort_values(by='Date', inplace=True)
            self.df['YearMonth'] = self.df['Date'].dt.to_period('M')
            self.categorize_expenses()
        except Exception as e:
            print(f"Error processing {self.name}: {e}")
