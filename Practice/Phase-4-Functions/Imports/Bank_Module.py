# bank_module.py

class Bank:
    def __init__(self):
        self.balance = 0
        print("Inside constructor")

    def deposit(self, amount):
        self.balance += amount
        print("Balance after deposit:", self.balance)

    def withdraw(self, amount):
        self.balance -= amount
        print("Balance after withdrawal:", self.balance)