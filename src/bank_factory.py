import importlib

class BankFactory:
    @staticmethod
    def get_bank(bank_name, csv_path):
        try:
            module = importlib.import_module(f'src.{bank_name.lower()}')
            bank_class = getattr(module, bank_name.capitalize())
            return bank_class(bank_name, csv_path)
        except ImportError:
            raise ValueError(f"Bank type '{bank_name}' not recognized.")
