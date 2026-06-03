from extract import extract_data
from transform import transform_data
from load import load_to_postgres
from export import export_csv

def run_pipeline():

    df = extract_data("data/raw/Nike_Sales_Uncleaned.csv")
    df = transform_data(df)
    load_to_postgres(df)
    export_csv(df) 

    print("ETL Pipeline executed successfully.")

if __name__ == "__main__":
    run_pipeline()