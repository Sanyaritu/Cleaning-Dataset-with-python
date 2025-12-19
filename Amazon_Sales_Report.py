import pandas as pd
import matplotlib.pyplot as plt

# load file
df = pd.read_csv("Amazon Sale Report.csv")

# quick look
df.head()
cols_to_keep = [
    "Date",
    "Order ID",
    "Category",
    "Qty",
    "Amount",
    "Status",
    "ship-postal-code"
]

df = df[cols_to_keep]
# convert date
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m-%d-%Y",
    errors="coerce"
)

# remove empty rows
df = df.dropna(subset=["Date", "Amount"])

# remove duplicates
df = df.drop_duplicates()

# keep only delivered orders
df["Status"] = df["Status"].str.strip().str.lower()
df = df[df["Status"].str.contains("ship")]


#time feature
df["Month"] = df["Date"].dt.to_period("M")

#monthly revenue trend
monthly_revenue = df.groupby("Month")["Amount"].sum()
monthly_revenue_pct = monthly_revenue.pct_change() * 100
print("Monthly Revenue:")
print(monthly_revenue)

print("\nMonth-over-Month % Change:")
print(monthly_revenue_pct)
monthly_revenue.plot(kind="line")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

top_products = (
    df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_products
top_products.plot(kind="bar")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.show()
status_counts = df["Status"].value_counts()
status_counts
aov = df.groupby("Order ID")["Amount"].sum().mean()
aov
df.to_excel("Cleaned_Amazon_Sales.xlsx", index=False)

#creating clean file
df_clean = df.copy()

# Keep only useful columns
df_clean = df_clean[
    ["Order ID", "Date", "Product", "Status", "Quantity", "Amount"]
]

df_clean.to_excel("Clean_Amazon_Sales_Report.xlsx", index=False)


