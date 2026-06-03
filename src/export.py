def export_csv(df):

    output_file = (
        "data/processed/"
        "Nike_Sales_Cleaned.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"File generated: {output_file}"
    )