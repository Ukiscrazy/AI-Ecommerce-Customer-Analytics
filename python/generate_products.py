import pandas as pd
import random
from pathlib import Path

# ==============================
# Output Folder
# ==============================

project_root = Path(__file__).parent.parent
raw_folder = project_root / "data" / "raw"
raw_folder.mkdir(parents=True, exist_ok=True)

# ==============================
# Categories and Brands
# ==============================

categories = {
    "Electronics": ["Samsung", "Apple", "Sony", "Boat", "Realme"],
    "Fashion": ["Nike", "Adidas", "Puma", "Levis", "Zara"],
    "Home": ["Philips", "Prestige", "Milton", "Cello"],
    "Beauty": ["Lakme", "Maybelline", "Loreal", "Nivea"],
    "Sports": ["Yonex", "Cosco", "Nike", "Puma"],
    "Books": ["Penguin", "Harper", "Oxford", "McGraw"],
    "Grocery": ["Amul", "Nestle", "Tata", "Aashirvaad"]
}

products = []

product_id = 1

for category, brands in categories.items():

    for i in range(70):

        brand = random.choice(brands)

        product_name = f"{brand} {category} Product {i+1}"

        cost_price = random.randint(200, 5000)

        price = round(cost_price * random.uniform(1.15, 1.60), 2)

        stock = random.randint(20, 500)

        rating = round(random.uniform(3.5, 5.0), 1)

        supplier = random.choice([
            "ABC Suppliers",
            "Global Traders",
            "Prime Distributors",
            "Smart Wholesale",
            "India Supply Hub"
        ])

        launch_date = pd.Timestamp(
            random.randint(2021, 2025),
            random.randint(1, 12),
            random.randint(1, 28)
        )

        products.append([
            product_id,
            product_name,
            category,
            brand,
            price,
            cost_price,
            stock,
            rating,
            supplier,
            launch_date
        ])

        product_id += 1

# ==============================
# DataFrame
# ==============================

products_df = pd.DataFrame(products, columns=[
    "product_id",
    "product_name",
    "category",
    "brand",
    "price",
    "cost_price",
    "stock",
    "rating",
    "supplier",
    "launch_date"
])

# ==============================
# Save CSV
# ==============================

output_file = raw_folder / "products.csv"

products_df.to_csv(output_file, index=False)

print("=" * 50)
print("Products dataset generated successfully!")
print("=" * 50)
print("Saved to:", output_file)
print("Total Products:", len(products_df))
print()
print(products_df.head())