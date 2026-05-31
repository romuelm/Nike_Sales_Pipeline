import pandas as pd
from sqlalchemy import create_engine
# 1. Load Data
df = pd.read_csv('Nike_Sales_Uncleaned.csv')
print(f"Original Shape: {df.shape}")

# 2. Cleaning of the Region Column
df['Region'] = df['Region'].str.title()
region_mapping = {
    'Hyd' : 'Hyderabad',
    'Hyderbad' : 'Hyderabad',
    'Bengaluru' : 'Bangalore'
}
df['Region'] = df['Region'].replace(region_mapping)

# 3.Handling Missing Values for Units_Sold Column
df['Units_Sold'] = df['Units_Sold'].fillna(1)

# 4. Connecting to PostgreSQL and Upload
print("Connecting to database...")
# Format: postgresql://user:password@host:port/database_name
engine = create_engine('postgresql://admin:password@localhost:5432/nike_sales')

# Write the dataframe to a SQL table named 'sales_data'
df.to_sql('sales_data', engine, if_exists='replace', index=False)
print("Success! Data loaded into PostgreSQL.")
