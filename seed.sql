INSERT INTO customers (name, email) VALUES
('Rahul Sharma', 'rahul.sharma@gmail.com'),
('Priya Verma', 'priya.verma@gmail.com'),
('Arjun Reddy', 'arjun.reddy@gmail.com'),
('Sneha Iyer', 'sneha.iyer@gmail.com'),
('Karan Mehta', 'karan.mehta@gmail.com');
INSERT INTO accounts (customer_id, account_type, balance) VALUES
(1, 'savings', 85000.00),
(2, 'current', 150000.00),
(3, 'savings', 45000.00),
(4, 'savings', 72000.00),
(5, 'current', 210000.00);
INSERT INTO transactions (account_id, amount, type, transaction_date, description) VALUES
(1, 50000, 'credit', '2026-01-05', 'Salary Credit'),
(1, 5000, 'debit', '2026-01-07', 'ATM Withdrawal'),
(1, 2000, 'debit', '2026-01-10', 'Online Shopping'),
(2, 120000, 'credit', '2026-01-03', 'Client Payment'),
(2, 20000, 'debit', '2026-01-15', 'Office Rent'),
(3, 30000, 'credit', '2026-01-01', 'Freelance Payment'),
(3, 5000, 'debit', '2026-01-09', 'Electricity Bill'),
(4, 70000, 'credit', '2026-01-04', 'Salary Credit'),
(4, 3000, 'debit', '2026-01-11', 'Groceries'),
(5, 200000, 'credit', '2026-01-02', 'Business Revenue'),
(5, 50000, 'debit', '2026-01-18', 'Supplier Payment');
INSERT INTO transactions (account_id, amount, type, transaction_date, description) VALUES
(1, 1500, 'debit', '2026-01-12', 'UPI Payment'),
(1, 2200, 'debit', '2026-01-14', 'Fuel'),
(1, 10000, 'credit', '2026-01-20', 'Bonus Credit'),
(1, 3500, 'debit', '2026-01-25', 'Restaurant'),

(2, 40000, 'credit', '2026-01-22', 'Project Payment'),
(2, 15000, 'debit', '2026-01-24', 'Office Supplies'),
(2, 8000, 'debit', '2026-01-26', 'Internet Bill'),
(2, 60000, 'credit', '2026-02-01', 'Client Transfer'),

(3, 7000, 'debit', '2026-01-12', 'Mobile Recharge'),
(3, 15000, 'credit', '2026-01-18', 'Part-time Income'),
(3, 2000, 'debit', '2026-01-21', 'Groceries'),
(3, 5000, 'debit', '2026-01-29', 'Online Purchase'),

(4, 4500, 'debit', '2026-01-13', 'Medical Expense'),
(4, 12000, 'credit', '2026-01-19', 'Freelance Work'),
(4, 3000, 'debit', '2026-01-27', 'Electricity Bill'),
(4, 25000, 'credit', '2026-02-02', 'Performance Bonus'),

(5, 75000, 'credit', '2026-01-21', 'Investor Funding'),
(5, 20000, 'debit', '2026-01-23', 'Equipment Purchase'),
(5, 15000, 'debit', '2026-01-28', 'Marketing Expense'),
(5, 50000, 'credit', '2026-02-03', 'Business Profit');