import numpy as np
import pandas as pd

# -----------------------------
# Random Seed
# -----------------------------
np.random.seed(42)

N = 1_000_000

# -----------------------------
# Sales Date
# -----------------------------
dates = pd.date_range(
    "2024-01-01",
    "2025-12-31",
    freq="H"
)

sale_date = np.random.choice(dates, N)

# -----------------------------
# Product Category
# -----------------------------
categories = np.random.choice(
    ["Electronics",
     "Furniture",
     "Clothing",
     "Food",
     "Sports"],
    N,
    p=[0.20,0.15,0.25,0.25,0.15]
)

# -----------------------------
# Quantity
# -----------------------------
quantity = np.random.poisson(
    lam=3,
    size=N
) + 1

# -----------------------------
# Unit Price
# -----------------------------
unit_price = np.random.lognormal(
    mean=4.5,
    sigma=0.5,
    size=N
)

# -----------------------------
# Discount
# -----------------------------
discount = np.random.beta(
    2,
    10,
    size=N
)

# -----------------------------
# Shipping Cost
# -----------------------------
shipping = np.random.normal(
    50,
    15,
    size=N
)

shipping = np.clip(shipping,5,None)

# -----------------------------
# Unit Cost
# -----------------------------
margin = np.random.uniform(
    0.20,
    0.50,
    size=N
)

unit_cost = unit_price * (1-margin)

# -----------------------------
# Revenue
# -----------------------------
gross_sales = quantity * unit_price

net_sales = gross_sales * (1-discount)

# -----------------------------
# Profit
# -----------------------------
cost = quantity * unit_cost

profit = net_sales - cost - shipping

# -----------------------------
# Customer ID
# -----------------------------
customer_id = np.random.randint(
    100000,
    999999,
    size=N
)

# -----------------------------
# Build DataFrame
# -----------------------------
df = pd.DataFrame({

    "SaleDate":sale_date,
    "CustomerID":customer_id,
    "Category":categories,
    "Quantity":quantity,
    "UnitPrice":unit_price.round(2),
    "Discount":discount.round(3),
    "Shipping":shipping.round(2),
    "Revenue":net_sales.round(2),
    "Profit":profit.round(2)

})

print(df.head())

print(df.describe())

# -----------------------------
# Save CSV
# -----------------------------
df.to_csv(
    "synthetic_sales_1M.csv",
    index=False
)
