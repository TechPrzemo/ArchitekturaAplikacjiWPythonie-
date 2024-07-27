import pytest
from zad6_klasa_testy import BankAccount, NotABanknote

@pytest.fixture
def account_balance():
    return BankAccount(1000)

@pytest.mark.payin
def test_payin(account_balance):
    account_balance.payin(500)
    assert account_balance.balance_checking() == 1500
    
    with pytest.raises(NotABanknote):
        account_balance.payin(9)
        
    with pytest.raises(NotABanknote):
        account_balance.payin(20.07)
    
@pytest.mark.payout
def test_payout(account_balance):
    account_balance.payout(500)
    assert account_balance.balance_checking() == 500
    
    with pytest.raises(NotABanknote):
        account_balance.payout(9)
    
    with pytest.raises(NotABanknote):
        account_balance.payout(20.07)
        
    with pytest.raises(ValueError):
        account_balance.payout(1500)
    
@pytest.mark.balance_checking
def test_balance_checking(account_balance):
    assert account_balance.balance_checking()
