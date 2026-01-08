class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # private data

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance
