from sqlalchemy import create_engine


def load_to_postgres(df):

    engine = create_engine(
        "postgresql://admin:password@localhost:5432/nike_sales"
    )

    df.to_sql(
        "nike_sales",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully.")