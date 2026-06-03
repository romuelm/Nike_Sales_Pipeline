from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.pipeline import run_pipeline

with DAG(
    dag_id = "nike_sales_pipeline",
    start_date = datetime(2024, 1, 1),
    schedule = "@daily",
    catchup = False
) as dag:
    
    run_etl = PythonOperator(
        task_id = "run_pipeline",
        python_callable = run_pipeline
    )