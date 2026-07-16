import pandas as pd
import random
from pathlib import Path
from datetime import timedelta

# ==============================
# Project Paths
# ==============================

project_root = Path(__file__).parent.parent
raw_folder = project_root / "data" / "raw"

# ==============================
# Read Existing CSV Files
# ==============================

customers_df = pd.read_csv(raw_folder / "customers.csv")
products_df = pd.read_csv(raw_folder / "products.csv")

print("Customers Loaded :", len(customers_df))
print("Products Loaded :", len(products_df))
# ==============================
# Generate Orders
# ==============================

orders = []

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "COD",
    "Wallet"
]

statuses = [
    "Delivered",
    "Shipped",
    "Cancelled",
    "Returned"
]

for order_id in range(1, 20001):

    customer_id = random.randint(1, len(customers_df))

    order_date = pd.Timestamp(
        random.randint(2023, 2025),
        random.randint(1, 12),
        random.randint(1, 28)
    )

    orders.append([
        order_id,
        customer_id,
        order_date,
        random.choice(payment_methods),
        random.choice(statuses)
    ])

orders_df = pd.DataFrame(orders, columns=[
    "order_id",
    "customer_id",
    "order_date",
    "payment_method",
    "order_status"
])

orders_df.to_csv(raw_folder / "orders.csv", index=False)

print()
print("Orders Generated Successfully")
print(orders_df.head())