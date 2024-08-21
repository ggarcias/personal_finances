import pytest
from src.bank_factory import BankFactory
from src.openbank import Openbank
from src.revolut import Revolut

def test_get_bank_openbank():
    bank = BankFactory.get_bank('Openbank', 'data/openbank_junio-agosto.csv')
    assert isinstance(bank, Openbank)
    assert bank.name == 'Openbank'

def test_get_bank_revolut():
    bank = BankFactory.get_bank('Revolut', 'data/revolut_junio-agosto.csv')
    assert isinstance(bank, Revolut)
    assert bank.name == 'Revolut'

def test_get_bank_invalid():
    with pytest.raises(ValueError):
        BankFactory.get_bank('InvalidBank', 'data/invalid.csv')
