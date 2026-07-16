# ============================================================
# AI-Powered E-commerce Intelligence Platform
# Generate Customer Dataset
# ============================================================

from faker import Faker
import pandas as pd
import random
from pathlib import Path

# Create Faker object (Indian data)
fake = Faker("en_IN")

# Number of customers
NUM_CUSTOMERS = 10000

# Store customer records
customers = []

# Generate customers
for customer_id in range(1, NUM_CUSTOMERS + 1):

    customer = {
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "gender": random.choice(["Male", "Female"]),
        "age": random.randint(18, 70),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
        "state": fake.state(),
        "signup_date": fake.date_between(start_date="-5y", end_date="today")
    }

    customers.append(customer)

# Convert to DataFrame
customers_df = pd.DataFrame(customers)

# ============================================================
# Create output folder automatically
# ============================================================

project_folder = Path(__file__).resolve().parent.parent
raw_folder = project_folder / "data" / "raw"

# Create folder if it doesn't exist
raw_folder.mkdir(parents=True, exist_ok=True)

# Save CSV
output_file = raw_folder / "customers.csv"
customers_df.to_csv(output_file, index=False)

# ============================================================
# Print Success Message
# ============================================================

print("=" * 50)
print("✅ Customers dataset generated successfully!")
print(f"📁 Saved at : {output_file}")
print(f"👥 Total Customers : {len(customers_df)}")
print("=" * 50)

print("\nFirst 5 Customers:\n")
print(customers_df.head())