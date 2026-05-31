import pandas as pd
from sqlalchemy import create_engine
# 1. Load Data
df = pd.read_csv('Nike_Sales_Uncleaned.csv')
print(f"Original Shape: {df.shape}")

# 2. Cleaning of the Region Column
df['Region'] = df['Region'].str.title().str.strip()
region_mapping = {
    'Hyd' : 'Hyderabad',
    'Hyderbad' : 'Hyderabad',
    'Bengaluru' : 'Bangalore'
}
df['Region'] = df['Region'].replace(region_mapping)

# 3. Data Corrections
# Order_Date Column fixing formats
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='mixed', errors='coerce')
df = df.dropna(subset=['Order_Date'])

# Remove corrupted rows (positive units sold but negative revenue)
df = df[~((df['Revenue'] < 0) & (df['Units_Sold'] > 0))]

# Correcting Negative Number
df['MRP'] = df['MRP'].abs()

# Capping of Discount Percentage
df.loc[df['Discount_Applied'] > 1, 'Discount_Applied'] = 1.0

# Handling Missing Values for Units_Sold Column and Size Column
df['Units_Sold'] = df['Units_Sold'].fillna(1)
df['Size'] = df['Size'].fillna('Unknown')

print(f"Cleaned Shape to Load: {df.shape}")


# 4. Connecting to PostgreSQL and Upload
print("Connecting to database...")
# Format: postgresql://user:password@host:port/database_name
engine = create_engine('postgresql://admin:password@localhost:5432/nike_sales')

# Write the dataframe to a SQL table named 'sales_data'
df.to_sql('sales_data', engine, if_exists='replace', index=False)
print("Success! Data loaded into PostgreSQL.")

# 5. Export Clean Data CSV
file_path = "Nike_Sales_Cleaned.csv"
df.to_csv(file_path, index=False)
print(f"File generated: {file_path}")
