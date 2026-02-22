import sqlite3

# Connect to database (creates it if not exists)
conn = sqlite3.connect("banking.db")
cursor = conn.cursor()

# Create tables
cursor.executescript("""
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    account_type TEXT,
    balance REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    amount REAL,
    type TEXT CHECK(type IN ('credit','debit')),
    date TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);
""")

# Insert sample data
cursor.executescript("""
INSERT INTO customers (name, email) VALUES
('John Doe', 'john@example.com'),
('Alice Smith', 'alice@example.com');

INSERT INTO accounts (customer_id, account_type, balance) VALUES
(1, 'Savings', 50000),
(2, 'Current', 75000);

INSERT INTO transactions (account_id, amount, type, date) VALUES
(1, 10000, 'credit', '2026-02-01'),
(1, 5000, 'debit', '2026-02-05'),
(1, 20000, 'credit', '2026-02-10'),
(2, 15000, 'debit', '2026-02-03'),
(2, 30000, 'credit', '2026-02-07');
""")

conn.commit()
conn.close()

print("✅ Database created and sample data inserted!")