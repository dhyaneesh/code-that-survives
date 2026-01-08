class CreditCard:
    def pay(self, amount):
        return f"Paid ₹{amount} using Credit Card"

class UPI:
    def pay(self, amount):
        return f"Paid ₹{amount} using UPI"

class Wallet:
    def pay(self, amount):
        return f"Paid ₹{amount} using Wallet"

# Same interface, different behavior
payments = [CreditCard(), UPI(), Wallet()]

for payment in payments:
    print(payment.pay(500))
