import pandas as pd

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

# 4. Save Cleaned Data to a new file
df.to_csv('Nike_Sales_Cleaned.csv', index=False)