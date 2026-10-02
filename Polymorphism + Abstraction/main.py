"""Payment processing example: abstraction and runtime polymorphism in Python."""

from abc import ABC, abstractmethod


class Payment(ABC):
    """Abstract base class. Every payment method must implement pay()."""

    def __init__(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.amount = amount

    @abstractmethod
    def pay(self):
        """Process the payment. Each subclass provides its own version."""


class CreditCardPayment(Payment):
    def __init__(self, amount, card_number, card_holder):
        super().__init__(amount)
        self.card_number = card_number
        self.card_holder = card_holder

    def pay(self):
        masked = "**** **** **** " + self.card_number[-4:]
        print(f"Credit Card: Rs.{self.amount:.2f} paid by {self.card_holder} using card {masked}")


class UPIPayment(Payment):
    def __init__(self, amount, upi_id):
        super().__init__(amount)
        self.upi_id = upi_id

    def pay(self):
        print(f"UPI: Rs.{self.amount:.2f} paid using UPI ID {self.upi_id}")


class NetBankingPayment(Payment):
    def __init__(self, amount, bank_name, account_holder):
        super().__init__(amount)
        self.bank_name = bank_name
        self.account_holder = account_holder

    def pay(self):
        print(f"Net Banking: Rs.{self.amount:.2f} paid by {self.account_holder} via {self.bank_name}")


def process_payment(payment: Payment):
    """Works with ANY Payment object. The correct pay() is chosen at runtime."""
    payment.pay()


if __name__ == "__main__":
    # 1. Abstract class cannot be instantiated
    try:
        Payment(100)
    except TypeError as error:
        print(f"Cannot create Payment object: {error}\n")

    # 2. Runtime polymorphism: same method call, different behaviour
    payments = [
        CreditCardPayment(2500, "1234567812345678", "Hrishabh Singh Tomar"),
        UPIPayment(799.50, "hrishabh@upi"),
        NetBankingPayment(15000, "State Bank of India", "Hrishabh Singh Tomar"),
    ]

    for payment in payments:
        process_payment(payment)