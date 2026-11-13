import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. Connect to our local MySQL database 
engine = create_engine("mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/fintech_churn_db")

# 2. Pull the clean data metrics we calculated using our SQL query
print(" Fetching engineered metrics from MySQL...")
df = pd.read_sql("SELECT merchant_id, ROUND(SUM(quantity * unit_price), 2) AS total_volume, COUNT(DISTINCT transaction_id) AS tx_count, DATEDIFF((SELECT MAX(transaction_time) FROM merchant_transactions), MAX(transaction_time)) AS days_inactive, DATEDIFF(MAX(transaction_time), MIN(transaction_time)) AS tenure FROM merchant_transactions GROUP BY merchant_id;", con=engine)

# 3. These are the columns we want our machine learning model to look at
features = ['total_volume', 'tx_count', 'days_inactive', 'tenure']

# 4. Fix the scale issue: convert huge volume numbers and tiny counts to a fair playing field so the math doesn't break
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[features])

# 5. Tell the K-Means algorithm to automatically find 3 distinct groups of merchants
print(" Running K-Means Machine Learning engine...")
model = KMeans(n_clusters=3, random_state=42)
df['risk_cluster'] = model.fit_predict(scaled_data)

# 6. Save our final results into a fresh CSV file for our Power BI dashboard
df.to_csv('merchant_predictions.csv', index=False)
print(" SUCCESS: Saved 'merchant_predictions.csv' with scaled ML clusters!")
