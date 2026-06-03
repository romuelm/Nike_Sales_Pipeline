from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Let Airflow know where to find your 'src' and 'data' folders
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.pipeline import run_pipeline

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
}

with DAG(
    'nike_sales_pipeline',
    default_args=default_args,
    schedule='@daily',  # <--- Changed this line!
    catchup=False,
) as dag:

    run_etl = PythonOperator(
        task_id='run_pipeline',
        python_callable=run_pipeline,
    )