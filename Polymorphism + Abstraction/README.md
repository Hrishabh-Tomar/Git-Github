# Payment Processing System

A Python example of **abstraction** and **runtime polymorphism** using an abstract `Payment` class.

## Classes

| Class | Purpose |
|-------|---------|
| `Payment` (abstract) | Defines the abstract `pay()` method every payment type must implement |
| `CreditCardPayment` | Pays using a masked card number |
| `UPIPayment` | Pays using a UPI ID |
| `NetBankingPayment` | Pays through a bank account |

## Concepts Demonstrated

- **Abstraction:** `Payment` uses `ABC` and `@abstractmethod`, so it cannot be instantiated and forces subclasses to implement `pay()`.
- **Runtime polymorphism:** `process_payment(payment)` calls `payment.pay()` on any `Payment` object, and Python picks the right version at runtime.

## Run

```bash
python main.py
```

## Sample Output

```
Cannot create Payment object: Can't instantiate abstract class Payment without an implementation for abstract method 'pay'

Credit Card: Rs.2500.00 paid by Hrishabh Singh Tomar using card **** **** **** 5678
UPI: Rs.799.50 paid using UPI ID hrishabh@upi
Net Banking: Rs.15000.00 paid by Hrishabh Singh Tomar via State Bank of India
```

## Author

Hrishabh Singh Tomar
