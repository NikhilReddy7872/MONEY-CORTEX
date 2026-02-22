balance = 50000

transactions = [
    {"amount": 10000, "type": "credit", "date": "2024-02-01"},
    {"amount": 5000, "type": "debit", "date": "2024-02-10"},
    {"amount": 3000, "type": "debit", "date": "2024-02-15"},
]

def get_balance():
    return balance

def get_transactions():
    return transactions

def get_monthly_spending():
    monthly = {}
    for tx in transactions:
        if tx["type"] == "debit":
            month = tx["date"][:7]
            monthly[month] = monthly.get(month, 0) + tx["amount"]
    return monthly