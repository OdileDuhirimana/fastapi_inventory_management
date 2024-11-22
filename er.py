# Import libraries
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_URL = "http://127.0.0.1:8000"

# 1. Fetch Data
def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}/")
    response.raise_for_status()
    return response.json()

# Fetch data from the API
products = fetch_data("products")
orders = fetch_data("orders")
customers = fetch_data("customers")

# 2. Load Data into DataFrames
products_df = pd.DataFrame(products)
orders_df = pd.DataFrame(orders)
customers_df = pd.DataFrame(customers)

print("Products DataFrame:")
print(products_df.head())

print("Orders DataFrame:")
print(orders_df.head())

print("Customers DataFrame:")
print(customers_df.head())

# 3. Perform Joins
# Merge orders with customers
orders_customers_df = pd.merge(orders_df, customers_df, left_on="user_id", right_on="id", how="left")
print("Orders + Customers DataFrame:")
print(orders_customers_df.head())

# Merge orders with products (via order items if needed)
order_items = fetch_data("order_items")  # Assuming a separate endpoint for order items
order_items_df = pd.DataFrame(order_items)

merged_orders_df = pd.merge(order_items_df, products_df, left_on="product_id", right_on="id", how="inner")
print("Merged Orders DataFrame (Order Items + Products):")
print(merged_orders_df.head())

# 4. Compute Statistics
print("Statistics for Product Prices:")
print(products_df["price"].describe())

# Correlation Matrix
numerical_cols = products_df.select_dtypes(include=[np.number])
correlation_matrix = numerical_cols.corr()

sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix for Products")
plt.show()

# 5. Export Data to CSV
merged_orders_df.to_csv("inventory_merged_data.csv", index=False)
print("Merged inventory data exported to 'inventory_merged_data.csv'.")

# 6. Predict Stock Levels
# Predict product stock depletion rate
products_df = products_df.dropna(subset=["stock_level"])
X = products_df[["price"]]  # Use price as a predictor
y = products_df["stock_level"]

# Further analysis can be done for prediction tasks.
