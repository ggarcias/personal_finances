import pandas as pd

from tabulate import tabulate

from src.bank_factory import BankFactory
from src.plotting import plot_balances, plot_income_vs_expenses, plot_expense_categories

def load_banks(bank_files):
    return [BankFactory.get_bank(bank_file['bank_name'], bank_file['csv_path']) for bank_file in bank_files]

def calculate_totals(banks):
    total_spent = total_income = total_beginning_balance = total_ending_balance = 0
    combined_metrics = []

    for bank in banks:
        bank.to_standard()
        print(f"\n{'-'*40}\nProcessing Bank: {bank.name}\n{'-'*40}")
        df_monthly = bank.calculate_metrics(start_date="2024-06-01 12:00:00", end_date="2024-08-21 12:00:00")
        print(tabulate(df_monthly, headers='keys', tablefmt='psql'))

        total_spent += df_monthly['Total_Expense'].sum()
        total_income += df_monthly['Total_Income'].sum()
        total_beginning_balance += df_monthly['Balance_Beginning'].iloc[0]
        total_ending_balance += df_monthly['Balance_Ending'].iloc[-1]

        bank.save_data(bank.df, f"{bank.name}_metrics", 'results/')
        combined_metrics.append(df_monthly)

    return total_income, total_spent, total_beginning_balance, total_ending_balance, combined_metrics

def compute_summary_stats(total_income, total_spent, overall_balance_change, savings_rate):
    summary_stats = pd.DataFrame({
        "Metric": ["Total Income", "Total Expense", "Overall Balance Change", "Savings Rate (Average)"],
        "Value": [total_income, total_spent, overall_balance_change, savings_rate]
    })
    return summary_stats

def main():
    bank_files = [
        {"csv_path": "data/openbank_junio-agosto.csv", "bank_name": "Openbank"},
        {"csv_path": "data/revolut_junio-agosto.csv", "bank_name": "Revolut"}
    ]

    banks = load_banks(bank_files)
    total_income, total_spent, total_beginning_balance, total_ending_balance, combined_metrics = calculate_totals(banks)

    overall_balance_change = total_ending_balance - total_beginning_balance

    combined_metrics_df = pd.concat(combined_metrics).groupby('YearMonth').sum().reset_index()
    combined_metrics_df['Savings_Rate'] = (combined_metrics_df['Total_Income'] - combined_metrics_df['Total_Expense']) / combined_metrics_df['Total_Income']
    combined_metrics_df.to_csv('results/combined_metrics.csv', index=False)

    print(f"\n{'='*40}\nCombined Monthly Metrics\n{'='*40}")
    print(tabulate(combined_metrics_df, headers='keys', tablefmt='psql'))

    summary_stats = compute_summary_stats(total_income, total_spent, overall_balance_change, combined_metrics_df['Savings_Rate'].mean())
    
    print(f"\n{'='*40}\nSummary Statistics\n{'='*40}")
    print(tabulate(summary_stats, headers='keys', tablefmt='psql'))

    summary_stats.to_csv('results/summary_statistics.csv', index=False)

    plot_balances(banks, 'results/')
    plot_income_vs_expenses(combined_metrics_df, 'results/')
    plot_expense_categories(banks, 'results/')

if __name__ == "__main__":
    main()
