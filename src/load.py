import os
from sqlalchemy import create_engine

def load_to_postgres(df):
    # Fallback to localhost if DB_HOST isn't specified (keeps your local terminal script working)
    db_host = os.getenv("TARGET_DB_HOST", "localhost")

    # The connection string now uses Airflow's default credentials and database
    engine = create_engine(
        f"postgresql://airflow:airflow@{db_host}:5432/nike_sales"
    )

    df.to_sql(
        "nike_sales", 
        engine, 
        if_exists="replace", 
        index=False
    )
    
    print(f"Cleaned Dataframe: {df.shape}")
    print("Data loaded successfully.")