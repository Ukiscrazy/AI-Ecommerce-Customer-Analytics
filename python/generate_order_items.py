import pandas as pd
import random
from pathlib import Path

# =====================================
# Project Paths
# =====================================

project_root = Path(__file__).parent.parent
raw_folder = project_root / "data" / "raw"

# =====================================
# Read Existing CSV Files
# =====================================

orders_df = pd.read_csv(raw_folder / "orders.csv")
products_df = pd.read_csv(raw_folder / "products.csv")

print("Orders Loaded :", len(orders_df))
print("Products Loaded :", len(products_df))

# =====================================
# Generate Order Items
# =====================================

order_items = []

item_id = 1

for _, order in orders_df.iterrows():

    # Each order contains 1 to 5 products
    number_of_products = random.randint(1, 5)

    selected_products = products_df.sample(number_of_products)

    for _, product in selected_products.iterrows():

        quantity = random.randint(1, 3)

        discount = random.choice([0, 5, 10, 15, 20])

        unit_price = product["price"]

        total_amount = round(
            quantity * unit_price * (1 - discount / 100),
            2
        )

        order_items.append([
            item_id,
            order["order_id"],
            product["product_id"],
            quantity,
            round(unit_price, 2),
            discount,
            total_amount
        ])

        item_id += 1

# =====================================
# DataFrame
# =====================================

order_items_df = pd.DataFrame(order_items, columns=[
    "item_id",
    "order_id",
    "product_id",
    "quantity",
    "unit_price",
    "discount_percent",
    "total_amount"
])

# =====================================
# Save CSV
# =====================================

order_items_df.to_csv(
    raw_folder / "order_items.csv",
    index=False
)

print()
print("=" * 50)
print("Order Items Generated Successfully")
print("=" * 50)
print("Total Rows :", len(order_items_df))
print()
print(order_items_df.head())