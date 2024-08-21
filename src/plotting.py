# src/plotting.py

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

def plot_balances(banks, output_folder):
    num_banks = len(banks)
    colors = plt.cm.get_cmap('tab10', num_banks)

    fig = plt.figure(figsize=(10, 4 * (num_banks + 1)))
    gs = GridSpec(num_banks + 1, 1, figure=fig)
    
    total_balance = None

    for i, bank in enumerate(banks):
        balance = bank.df[['Date', 'Balance']].copy()
        balance['Date'] = pd.to_datetime(balance['Date'])
        balance.set_index('Date', inplace=True)
        balance = balance[~balance.index.duplicated(keep='last')]
        balance = balance.resample('D').ffill()

        ax = fig.add_subplot(gs[i, 0])
        ax.plot(balance.index, balance['Balance'], label=bank.name, color=colors(i))
        ax.set_title(f'{bank.name} Balance Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Balance')
        ax.legend()
        ax.grid(True)

        if total_balance is None:
            total_balance = balance['Balance']
        else:
            total_balance += balance['Balance']

    ax_total = fig.add_subplot(gs[num_banks, 0])
    ax_total.plot(total_balance.index, total_balance, label='Total Balance', linestyle='--', color='black')
    ax_total.set_title('Total Balance Over Time')
    ax_total.set_xlabel('Date')
    ax_total.set_ylabel('Balance')
    ax_total.legend()
    ax_total.grid(True)

    plt.subplots_adjust(hspace=0.5)
    plt.savefig(f"{output_folder}/balance_plot.png")
    plt.close()


def plot_income_vs_expenses(df, output_folder):
    plt.figure(figsize=(10, 6))
    plt.plot(df['YearMonth'].dt.to_timestamp(), df['Total_Income'], label='Total Income', color='green', marker='o')
    plt.plot(df['YearMonth'].dt.to_timestamp(), df['Total_Expense'], label='Total Expense', color='red', marker='o')
    plt.title('Monthly Income vs Expenses')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{output_folder}/income_vs_expenses_plot.png")
    plt.close()


def plot_expense_categories(banks, output_folder):
    num_banks = len(banks)
    
    # Set up the GridSpec layout
    fig = plt.figure(figsize=(12, 6 + 4 * num_banks))
    gs = GridSpec(num_banks + 1, 1, figure=fig)
    
    # Combine all bank data into one DataFrame for the total plot
    all_expenses = pd.concat([bank.df for bank in banks])
    
    # Plot each bank's expense categories
    for i, bank in enumerate(banks):
        # Filter for only expenses (negative amounts) for the bank
        expense_categories = bank.df[bank.df['Amount'] < 0]
        
        # Group by category and sum the expenses
        category_totals = expense_categories.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
        
        # Create subplot for the individual bank
        ax = fig.add_subplot(gs[i, 0])
        sns.barplot(x=category_totals.values, y=category_totals.index, hue=category_totals.index, palette='Blues_d', ax=ax, legend=False)
        ax.set_title(f'Total Expenses by Category - {bank.name}', fontsize=14)
        ax.set_xlabel('Total Amount Spent (€)', fontsize=12)
        ax.set_ylabel('Category', fontsize=12)
        
        # Add annotations to each bar
        for j in range(len(category_totals)):
            ax.text(category_totals.values[j], j, f'{category_totals.values[j]:.2f}€', va='center', ha='left', fontsize=10)
        
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Plot for combined total expenses
    expense_categories_total = all_expenses[all_expenses['Amount'] < 0]
    category_totals_total = expense_categories_total.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
    
    # Create subplot for the combined total
    ax_total = fig.add_subplot(gs[num_banks, 0])
    sns.barplot(x=category_totals_total.values, y=category_totals_total.index, hue=category_totals_total.index, palette='Blues_d', ax=ax_total, legend=False)
    ax_total.set_title('Total Expenses by Category - Combined', fontsize=14)
    ax_total.set_xlabel('Total Amount Spent (€)', fontsize=12)
    ax_total.set_ylabel('Category', fontsize=12)
    
    # Add annotations to each bar for the total plot
    for j in range(len(category_totals_total)):
        ax_total.text(category_totals_total.values[j], j, f'{category_totals_total.values[j]:.2f}€', va='center', ha='left', fontsize=10)
    
    ax_total.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(f"{output_folder}/expense_categories_by_bank_and_total.png")
    plt.close()
