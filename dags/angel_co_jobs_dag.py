from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from helpers import SqlQueries
from crawlers.angel_co import main as angel_co_crawler

default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2019, 8, 21),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('angel_co_jobs_dag',
          default_args=default_args,
          description='Load the jobs dataset and insert into Redshift',
          schedule_interval='@daily'
        )

run_selenium_crawler = PythonOperator(
    task_id='run_selenium_crawler',
    provide_context=False,
    python_callable=angel_co_crawler
)
