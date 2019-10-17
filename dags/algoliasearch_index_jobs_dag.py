from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2019, 8, 21),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('algoliasearch_index_jobs_dag',
          default_args=default_args,
          description='Index all jobs from our PostgreSQL database',
          schedule_interval='@daily'
        )


