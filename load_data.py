import pandas as pd
from sqlalchemy import create_engine

print("Reading 'fintech_data.csv'...")
df = pd.read_csv('fintech_data.csv')

# 1. Connect to MySQL 
engine = create_engine("mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/fintech_churn_db")

print("loading data into MySQL...")
# 2. Push the data in one single fast move. 

df.to_sql(name='merchant_transactions', con=engine, if_exists='replace', index=False)

print("SUCCESS: Data loaded perfectly into 'merchant_transactions' table!")
