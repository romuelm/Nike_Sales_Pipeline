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

# Intelligent Fill for Missing Prices (MRP) - Kaggle Method
# Fills missing prices based on the median price of that specific product
df["MRP"] = df.groupby("Product_Name")["MRP"].transform(lambda x: x.fillna(x.median()))
df["MRP"] = df.groupby("Product_Line")["MRP"].transform(lambda x: x.fillna(x.median()))

# Capping of Discount Percentage and filling the blanks with 0
df['Discount_Applied'] = df['Discount_Applied'].fillna(0)
df.loc[df['Discount_Applied'] > 1, 'Discount_Applied'] = 1.0


# Handling Missing & Negative Values for Units_Sold
df['Units_Sold'] = df['Units_Sold'].fillna(df['Units_Sold'].median())
df.loc[df["Units_Sold"] < 0, "Units_Sold"] = 0

# Size Clean-up (Kaggle Method: Map Shoe Sizes to Apparel Sizes)
df["Size"] = df["Size"].astype(str).str.strip().str.upper()
df["Size"] = df["Size"].replace(["NAN", "NONE", "ERROR", "UNKNOWN", ""], np.nan)

# Separate numeric sizes from categorical sizes
numeric_mask = df["Size"].str.match(r"^\d+$", na=False)
df["Size_Num"] = df["Size"].where(numeric_mask)
df["Size_Cat"] = df["Size"].where(~numeric_mask)
df["Size_Num"] = pd.to_numeric(df["Size_Num"], errors="coerce")

# Function to map shoe numbers to S/M/L/XL
def map_num_to_cat(x):
    if pd.isna(x): return np.nan
    elif x <= 7: return "S"
    elif x <= 9: return "M"
    elif x <= 11: return "L"
    else: return "XL"

# Apply mapping and fill missing values with the mode (most common size)
df.loc[df["Size_Cat"].isna(), "Size_Cat"] = df["Size_Num"].apply(map_num_to_cat)
df["Size_Cat"] = df["Size_Cat"].fillna(df["Size_Cat"].mode()[0])

# Encode to 0, 1, 2, 3 
size_order = ["S", "M", "L", "XL"]
df["Size_Cat"] = pd.Categorical(df["Size_Cat"], categories=size_order, ordered=True)
df["Size_Cat_Encoded"] = df["Size_Cat"].cat.codes

# Drop intermediate columns (we keep Size_Cat for Power BI labels)
df.drop(columns=['Size', 'Size_Num'], inplace=True)

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
