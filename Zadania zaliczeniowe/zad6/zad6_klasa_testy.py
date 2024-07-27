"""
Napisz klasę BankAccount, która implementuje podstawowe operacje na koncie
bankowym, takie jak wpłacanie, wypłacanie i sprawdzanie salda. Klasa powinna
wywoływać wyjątek przy próbie wpłaty lub wypłaty niepoprawnej kwoty. Następnie napisz
testy jednostkowe za pomocą PyTest, które sprawdzą poprawność działania metod oraz
obsługę błędów.
"""

class BankAccount:
    def __init__(self, balance):
        self.current_balance = balance
          
    def payin(self, amount):
        if amount % 10 != 0: 
            raise NotABanknote(f"Próbujesz wpłacić kwotę, która nie jest banknotem/banknotami!!! ")
        self.current_balance += amount
        return self.current_balance
        
    def payout(self, amount):
        if amount % 10 != 0: 
            raise NotABanknote(f"Próbujesz wypłacić kwotę, która nie jest banknotem/banknotami!!! ")
        if self.current_balance - amount < 0:
            raise ValueError(f"Nie można wypłacić więcej z konta niż się posiada!!!")
        self.current_balance -= amount
        return self.current_balance
        
    def balance_checking(self):
        return self.current_balance

class NotABanknote(Exception):
    pass

if __name__ == '__main__':
    account = BankAccount(1000)
    print(account.balance_checking())
    account.payin(0)
    print(account.balance_checking())
    account.payout(1500)
    print(account.balance_checking())