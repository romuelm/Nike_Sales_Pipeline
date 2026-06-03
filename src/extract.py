import pandas as pd 

def extract_data(file_path):
    print("Loading Dataset...")
    df = pd.read_csv(file_path)
    print(f"Original Shape: {df.shape}")

    return df
    