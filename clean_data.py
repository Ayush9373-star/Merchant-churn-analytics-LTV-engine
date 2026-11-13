import pandas as pd

# LOAD THE RAW DATA

print(" Reading 'data.csv'...")
# (encoding handles special currency symbols safely)
df = pd.read_csv('data.csv', encoding='ISO-8859-1')



# Check for missing identities
missing_ids = df['CustomerID'].isnull().sum()
print(f"   • Missing Customer IDs found: {missing_ids} rows")

# Check for anomalies (Free items or test data)
zero_prices = (df['UnitPrice'] <= 0).sum()
print(f"   • Broken/Free items (Price <= 0): {zero_prices} rows")

# Check for refunds (Negative quantities)
refunds_count = (df['Quantity'] < 0).sum()
print(f"   • Refunds / Chargebacks found: {refunds_count} rows")


# Remove rows where CustomerID is missing
df_clean = df.dropna(subset=['CustomerID'])

# Remove rows where any of the other columns are missing.
df_clean = df_clean.dropna()

# Remove duplicate rows (if any)
df_clean = df_clean.drop_duplicates()

# Convert text dates into real calendar timestamps
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])

# Standardize ID numbers into clean text format
df_clean['CustomerID'] = df_clean['CustomerID'].astype(int).astype(str)

# Fix 4: Remove broken/free items (Keep only real revenue transactions)
df_clean = df_clean[df_clean['UnitPrice'] > 0]

# If quantity is positive, it's a successful payment
df_sales = df_clean[df_clean['Quantity'] > 0]

# If quantity is negative, it's a refund/chargeback
df_refunds = df_clean[df_clean['Quantity'] < 0]

# Rename columns to  FinTech names
fintech_columns = {
    'CustomerID': 'merchant_id',
    'InvoiceNo': 'transaction_id',
    'InvoiceDate': 'transaction_time',
    'Quantity': 'quantity',
    'UnitPrice': 'unit_price'
}
df_sales = df_sales.rename(columns=fintech_columns)


# Keep only the columns we actually need for the next step
final_columns = ['merchant_id', 'transaction_id', 'transaction_time', 'quantity', 'unit_price']
df_sales[final_columns].to_csv('fintech_data.csv', index=False)

print("\n🚀 SUCCESS! The data is now audited and 100% clean.")
print(f"Saved 'fintech_data.csv' with {len(df_sales)} perfect rows!")
