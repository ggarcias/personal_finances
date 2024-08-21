import pytest
from main import load_banks, calculate_totals, compute_summary_stats

def test_load_banks():
    bank_files = [
        {"csv_path": "data/openbank_junio-agosto.csv", "bank_name": "Openbank"},
        {"csv_path": "data/revolut_junio-agosto.csv", "bank_name": "Revolut"}
    ]
    banks = load_banks(bank_files)
    assert len(banks) == 2

def test_calculate_totals():
    bank_files = [
        {"csv_path": "data/openbank_junio-agosto.csv", "bank_name": "Openbank"},
        {"csv_path": "data/revolut_junio-agosto.csv", "bank_name": "Revolut"}
    ]
    banks = load_banks(bank_files)
    total_income, total_spent, total_beginning_balance, total_ending_balance, combined_metrics = calculate_totals(banks)
    assert total_income > 0
    assert total_spent > 0
    assert total_ending_balance >= total_beginning_balance

def test_compute_summary_stats():
    summary_stats = compute_summary_stats(1000, 500, 500, 0.5)
    assert summary_stats["Value"][0] == 1000
    assert summary_stats["Value"][1] == 500
    assert summary_stats["Value"][2] == 500
    assert summary_stats["Value"][3] == 0.5
